# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/note_settings_component.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
import math
from functools import partial
from itertools import ifilter, imap, chain, izip_longest
from ableton.v2.base import clamp, find_if, forward_property, listenable_property, listens, listens_group, liveobj_valid, task
from ableton.v2.control_surface import defaults, Component
from ableton.v2.control_surface.control import ButtonControl, ControlManager, control_list, EncoderControl, StepEncoderControl
from ableton.v2.control_surface.elements import DisplayDataSource
from ableton.v2.control_surface.mode import ModesComponent, Mode, AddLayerMode
from .consts import CHAR_ELLIPSIS, GRAPH_VOL

class NoteSettingBase(ControlManager):
    __events__ = (u'setting_changed', )
    attribute_index = -1
    encoder = EncoderControl()

    def __init__(self, grid_resolution=None, *a, **k):
        super(NoteSettingBase, self).__init__(*a, **k)
        self._min_max_value = None
        self._grid_resolution = grid_resolution
        return

    def encoder_value_to_attribute(self, value):
        raise NotImplementedError

    @property
    def step_length(self):
        if self._grid_resolution:
            return self._grid_resolution.step_length
        return 1.0

    def set_min_max(self, min_max_value):
        self._min_max_value = min_max_value

    @encoder.value
    def encoder(self, value, _):
        self._on_encoder_value_changed(value)

    def _on_encoder_value_changed(self, value):
        self.notify_setting_changed(self.attribute_index, self.encoder_value_to_attribute(value))


class NoteSetting(NoteSettingBase):

    def __init__(self, *a, **k):
        super(NoteSetting, self).__init__(*a, **k)
        self.value_source = DisplayDataSource()
        self.label_source = DisplayDataSource()
        self.label_source.set_display_string(self.get_label())

    def get_label(self):
        raise NotImplementedError

    def attribute_min_max_to_string(self, min_value, max_value):
        raise NotImplementedError

    def set_min_max(self, min_max_value):
        self.value_source.set_display_string(self.attribute_min_max_to_string(min_max_value[0], min_max_value[1]) if min_max_value else '-')


RANGE_STRING_FLOAT = '%.1f' + CHAR_ELLIPSIS + '%.1f'
RANGE_STRING_INT = '%d' + CHAR_ELLIPSIS + '%d'

def step_offset_percentage(step_length, value):
    return int(round((value - int(value / step_length) * step_length) / step_length * 100))


def step_offset_min_max_to_string(step_length, min_value, max_value):
    min_value = step_offset_percentage(step_length, min_value)
    max_value = step_offset_percentage(step_length, max_value)
    if min_value == max_value:
        return '%d%%' % min_value
    return (RANGE_STRING_INT + '%%') % (min_value, max_value)


def convert_value_to_graphic(value, value_range):
    value_bar = GRAPH_VOL
    graph_range = float(len(value_bar))
    value = clamp(int(value / value_range * graph_range), 0, len(value_bar) - 1)
    display_string = value_bar[value]
    return display_string


class NoteNudgeSetting(NoteSetting):
    attribute_index = 1

    def get_label(self):
        return 'Nudge'

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    def attribute_min_max_to_string(self, min_value, max_value):
        return step_offset_min_max_to_string(self.step_length, min_value, max_value)


class NoteLengthCoarseSetting(NoteSetting):
    attribute_index = 2
    encoder = StepEncoderControl()

    def get_label(self):
        return 'Length -'

    def attribute_min_max_to_string(self, min_value, max_value):
        min_value = min_value / self.step_length
        max_value = max_value / self.step_length

        def format_string(value):
            num_non_decimal_figures = int(math.log10(value)) if value > 0 else 0
            return '%%.%dg' % (num_non_decimal_figures + 2,)

        if min_value == max_value:
            return (format_string(min_value) + ' stp') % min_value
        return (format_string(min_value) + CHAR_ELLIPSIS + format_string(max_value)) % (
         min_value, max_value)

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    @encoder.value
    def encoder(self, value, _):
        self._on_encoder_value_changed(value)


class NoteLengthFineSetting(NoteSetting):
    attribute_index = 2

    def get_label(self):
        return 'Fine'

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    def attribute_min_max_to_string(self, min_value, max_value):
        value = step_offset_percentage(self.step_length, min_value)
        return convert_value_to_graphic(value, 100.0)


class NoteVelocitySetting(NoteSetting):
    attribute_index = 3

    def get_label(self):
        return 'Velocity'

    def encoder_value_to_attribute(self, value):
        return value * 128

    def attribute_min_max_to_string(self, min_value, max_value):
        if int(min_value) == int(max_value):
            return str(int(min_value))
        return RANGE_STRING_INT % (min_value, max_value)


class NoteSettingsComponentBase(Component):
    __events__ = (u'setting_changed', u'full_velocity')
    full_velocity_button = ButtonControl()

    def __init__(self, grid_resolution=None, *a, **k):
        super(NoteSettingsComponentBase, self).__init__(*a, **k)
        self._settings = []
        self._encoders = []
        self._create_settings(grid_resolution)

    def _create_settings(self, grid_resolution):
        self._add_setting(NoteNudgeSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteLengthCoarseSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteLengthFineSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteVelocitySetting(grid_resolution=grid_resolution))

    def _add_setting(self, setting):
        assert len(self._settings) < 8, 'Cannot show more than 8 settings'
        self._settings.append(setting)
        self._update_encoders()
        self.register_disconnectable(setting)
        self.register_slot(setting, self.notify_setting_changed, 'setting_changed')

    @property
    def number_of_settings(self):
        return len(self._settings)

    def set_info_message(self, message):
        pass

    def set_encoder_controls(self, encoders):
        self._encoders = encoders or []
        self._update_encoders()

    def set_min_max(self, index, min_max_value):
        setting_for_index = [ i for i in self._settings if i.attribute_index == index ]
        for setting in setting_for_index:
            setting.set_min_max(min_max_value)

    @full_velocity_button.pressed
    def full_velocity_button(self, button):
        if self.is_enabled():
            self.notify_full_velocity()

    def _update_encoders(self):
        if self.is_enabled() and self._encoders:
            for encoder, setting in izip_longest(self._encoders[-len(self._settings):], self._settings):
                setting.encoder.set_control_element(encoder)

        else:
            map(lambda setting: setting.encoder.set_control_element(None), self._settings)

    def update(self):
        super(NoteSettingsComponentBase, self).update()
        self._update_encoders()


class NoteSettingsComponent(NoteSettingsComponentBase):

    def __init__(self, *a, **k):
        super(NoteSettingsComponent, self).__init__(*a, **k)
        self._top_data_sources = [ DisplayDataSource() for _ in xrange(8) ]
        self._bottom_data_sources = [ DisplayDataSource() for _ in xrange(8) ]
        self._info_data_source = DisplayDataSource()
        self._create_display_sources()

    def _create_display_sources(self):
        self._top_data_sources = [ DisplayDataSource() for _ in xrange(8 - len(self._settings)) ] + [ s.label_source for s in self._settings ]
        self._bottom_data_sources = [ DisplayDataSource() for _ in xrange(8 - len(self._settings)) ] + [ s.value_source for s in self._settings ]

    def set_top_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources(self._top_data_sources)

    def set_bottom_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources(self._bottom_data_sources)

    def set_info_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources([self._info_data_source])

    def set_clear_display_line(self, display):
        if self.is_enabled() and display:
            display.reset()

    def set_info_message(self, message):
        self._info_data_source.set_display_string(message.rjust(62))


class DetailViewRestorerMode(Mode):
    u"""
    Restores the detail view if either only clip view or device view is visible.
    Has no effect if the detail view is hidden at the point the mode is entered.
    """

    def __init__(self, application=None, *a, **k):
        super(DetailViewRestorerMode, self).__init__(*a, **k)
        self._app = application
        self._view_to_restore = None
        return

    def enter_mode(self):
        clip_view_visible = self._app.view.is_view_visible('Detail/Clip', False)
        device_chain_visible = self._app.view.is_view_visible('Detail/DeviceChain', False)
        if clip_view_visible != device_chain_visible:
            self._view_to_restore = 'Detail/Clip' if clip_view_visible else 'Detail/DeviceChain'

    def leave_mode(self):
        try:
            if self._view_to_restore:
                self._app.view.show_view(self._view_to_restore)
                self._view_to_restore = None
        except RuntimeError:
            pass

        return


def show_clip_view(application):
    try:
        view = application.view
        if view.is_view_visible('Detail/DeviceChain', False) and not view.is_view_visible('Detail/Clip', False):
            application.view.show_view('Detail/Clip')
    except RuntimeError:
        pass


class ModeSelector(Component):
    select_buttons = control_list(ButtonControl, color='DefaultButton.Disabled')
    state_buttons = control_list(ButtonControl, color='DefaultButton.Disabled')


class NoteEditorSettingsComponent(ModesComponent):
    initial_encoders = control_list(EncoderControl)
    encoders = control_list(EncoderControl)

    def __init__(self, note_settings_component_class=None, automation_component_class=None, grid_resolution=None, initial_encoder_layer=None, encoder_layer=None, *a, **k):
        super(NoteEditorSettingsComponent, self).__init__(*a, **k)
        assert encoder_layer
        assert note_settings_component_class is not None
        assert automation_component_class is not None
        self.settings = note_settings_component_class(grid_resolution=grid_resolution, parent=self, is_enabled=False)
        self.automation = automation_component_class(parent=self, is_enabled=False)
        self._mode_selector = ModeSelector(parent=self, is_enabled=False)
        self._visible_detail_view = 'Detail/DeviceChain'
        self._show_settings_task = self._tasks.add(task.sequence(task.wait(defaults.MOMENTARY_DELAY), task.run(self._show_settings))).kill()
        self._update_infos_task = self._tasks.add(task.run(self._update_note_infos)).kill()
        self._settings_modes = ModesComponent(parent=self)
        self._settings_modes.set_enabled(False)
        self._settings_modes.add_mode('automation', [
         self.automation,
         self._mode_selector,
         partial(self._set_envelope_view_visible, True),
         partial(show_clip_view, self.application)])
        self._settings_modes.add_mode('note_settings', [
         self.settings,
         self._update_note_infos,
         self._mode_selector,
         partial(self._set_envelope_view_visible, False),
         partial(show_clip_view, self.application)])
        self._settings_modes.selected_mode = 'note_settings'
        self.__on_selected_setting_mode_changed.subject = self._settings_modes
        self.add_mode('disabled', [])
        self.add_mode('about_to_show', [
         AddLayerMode(self, initial_encoder_layer),
         (
          self._show_settings_task.restart, self._show_settings_task.kill)])
        self.add_mode('enabled', [
         DetailViewRestorerMode(self.application),
         AddLayerMode(self, encoder_layer),
         self._settings_modes])
        self.selected_mode = 'disabled'
        self._editors = []
        self._on_detail_clip_changed.subject = self.song.view
        self._on_selected_track_changed.subject = self.song.view
        self.__on_full_velocity_changed.subject = self.settings
        self.__on_setting_changed.subject = self.settings
        return

    automation_layer = forward_property('automation')('layer')
    mode_selector_layer = forward_property('_mode_selector')('layer')
    selected_setting = forward_property('_settings_modes')('selected_mode')

    @property
    def step_settings(self):
        return self._settings_modes

    @property
    def editors(self):
        return self._editors

    @listenable_property
    def is_touched(self):
        return any(imap(lambda e: e and e.is_touched, ifilter(lambda e: self._can_notify_is_touched(e), self.encoders)))

    def _is_step_held(self):
        return len(self._active_note_regions()) > 0

    def add_editor(self, editor):
        assert editor != None
        self._editors.append(editor)
        self._on_active_note_regions_changed.add_subject(editor)
        self._on_notes_changed.replace_subjects(self._editors)
        self.__on_modify_all_notes_changed.add_subject(editor)
        return

    def set_encoders(self, encoders):
        self.encoders.set_control_element(encoders)
        self.settings.set_encoder_controls(encoders)
        self.automation.set_parameter_controls(encoders)

    @property
    def parameter_provider(self):
        self.automation.parameter_provider

    @parameter_provider.setter
    def parameter_provider(self, value):
        self.automation.parameter_provider = value

    @listens('selected_mode')
    def __on_selected_setting_mode_changed(self, mode):
        if mode == 'automation':
            self.automation.selected_time = self._active_note_regions()

    def update_view_state_based_on_selected_setting(self, setting):
        if self.selected_mode == 'enabled' and self.is_touched or setting is None:
            self._set_settings_view_enabled(False)
        elif self._is_step_held():
            if self.selected_setting == 'automation' and self.automation.can_automate_parameters or self.selected_setting == 'note_settings':
                self._show_settings()
        return

    @listens('full_velocity')
    def __on_full_velocity_changed(self):
        for editor in self._editors:
            editor.set_full_velocity()

    @listens('setting_changed')
    def __on_setting_changed(self, index, value):
        for editor in self._editors:
            self._modify_note_property_offset(editor, index, value)

    def _modify_note_property_offset(self, editor, index, value):
        if index == 1:
            editor.set_nudge_offset(value)
        elif index == 2:
            editor.set_length_offset(value)
        elif index == 3:
            editor.set_velocity_offset(value)

    def _set_envelope_view_visible(self, visible):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip):
            if visible:
                clip.view.show_envelope()
            else:
                clip.view.hide_envelope()

    def _set_settings_view_enabled(self, should_show_view):
        really_show_view = should_show_view and self.automation.can_automate_parameters if self.selected_setting == 'automation' else should_show_view
        if really_show_view:
            if self.selected_mode == 'disabled':
                self.selected_mode = 'about_to_show'
        else:
            self._hide_settings()

    def _active_note_regions(self):
        all_active_regions = imap(lambda e: e.active_note_regions, self._editors)
        return list(set(chain.from_iterable(all_active_regions)))

    @listens_group('active_note_regions')
    def _on_active_note_regions_changed(self, _):
        if self.is_enabled():
            all_steps = self._active_note_regions()
            self.automation.selected_time = all_steps
            self._update_note_infos()
            self._set_settings_view_enabled(len(all_steps) > 0 and self.selected_setting != None or self.is_touched)
        return

    @listens_group('modify_all_notes')
    def __on_modify_all_notes_changed(self, editor):
        self.selected_mode = 'about_to_show' if editor.modify_all_notes_enabled else 'disabled'

    @listens_group('notes_changed')
    def _on_notes_changed(self, editor):
        self._update_infos_task.restart()

    @listens('detail_clip')
    def _on_detail_clip_changed(self):
        self.automation.clip = self.song.view.detail_clip if self.is_enabled() else None
        return

    @listens('selected_track')
    def _on_selected_track_changed(self):
        self.selected_mode = 'disabled'

    @initial_encoders.touched
    def initial_encoders(self, encoder):
        if self.selected_mode == 'about_to_show':
            self._show_settings()

    @initial_encoders.value
    def initial_encoders(self, encoder, value):
        if self.selected_mode == 'about_to_show':
            self._show_settings()

    @encoders.touched
    def encoders(self, encoder):
        if self._can_notify_is_touched(encoder):
            self.notify_is_touched()

    @encoders.released
    def encoders(self, encoder):
        if not self.is_touched and not self._is_step_held() and not self._is_edit_all_notes_active():
            self._hide_settings()
        if self._can_notify_is_touched(encoder):
            self.notify_is_touched()

    @encoders.value
    def encoders(self, encoder, value):
        self._notify_modification()

    def _can_notify_is_touched(self, encoder):
        if self.is_enabled():
            return self._settings_modes.selected_mode != 'note_settings' or encoder.index >= self.encoders.control_count - self.settings.number_of_settings
        return False

    def _is_edit_all_notes_active(self):
        return find_if(lambda e: e.modify_all_notes_enabled, self._editors) != None

    def _notify_modification(self):
        for editor in self._editors:
            editor.notify_modification()

    def _update_note_infos(self):
        if self.settings.is_enabled():

            def min_max((l_min, l_max), (r_min, r_max)):
                return (min(l_min, r_min), max(l_max, r_max))

            all_min_max_attributes = filter(None, imap(lambda e: e.get_min_max_note_values(), self._editors))
            min_max_values = [(99999, -99999)] * 4 if len(all_min_max_attributes) > 0 else None
            for min_max_attribute in all_min_max_attributes:
                for i, attribute in enumerate(min_max_attribute):
                    min_max_values[i] = min_max(min_max_values[i], attribute)

            for i in xrange(4):
                self.settings.set_min_max(i, min_max_values[i] if min_max_values else None)

            self.settings.set_info_message('Tweak to add note' if not self._is_edit_all_notes_active() and not min_max_values else '')
        return

    def _show_settings(self):
        if self.selected_mode != 'enabled':
            self.selected_mode = 'enabled'
            self._notify_modification()

    def _hide_settings(self):
        self.selected_mode = 'disabled'

    def on_enabled_changed(self):
        super(NoteEditorSettingsComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self.selected_mode = 'disabled'

    def update(self):
        super(NoteEditorSettingsComponent, self).update()
        if self.is_enabled():
            self._on_detail_clip_changed()