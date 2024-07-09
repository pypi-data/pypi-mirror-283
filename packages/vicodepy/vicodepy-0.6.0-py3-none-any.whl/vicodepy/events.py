# ViCodePy - A video coder for psychological experiments
#
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
)
from functools import partial
from .utils import color_fg_from_bg


class ChooseEvent(QDialog):
    def __init__(self, events=None):
        super().__init__()
        self.setWindowTitle("Choose event")
        layout = QFormLayout(self)
        eventbox = QHBoxLayout()
        for i, event in enumerate(events):
            button = QPushButton(event.name)
            bg_color = event.color
            fg_color = color_fg_from_bg(bg_color)
            button.setStyleSheet(
                f"background-color: {bg_color.name()} ;"
                f" color: {fg_color.name()}"
            )
            button.clicked.connect(partial(self.set_chosen, i))
            eventbox.addWidget(button)
        layout.addRow(eventbox)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def set_chosen(self, val):
        self.chosen = val
        self.accept()

    def get_chosen(self):
        return self.chosen
