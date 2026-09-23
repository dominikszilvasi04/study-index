from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from study_index.events.event_database import EventDatabase
from study_index.events.models import StudyEvent
from study_index.modules.module_database import ModuleDatabase


class EventListPage(QWidget):
    title_label: QLabel
    description_label: QLabel
    empty_message: QLabel
    events_list: QListWidget

    def __init__(self, event_database: EventDatabase, module_database: ModuleDatabase) -> None:
        super().__init__()
        self.setObjectName("eventListPage")
        self.event_database = event_database
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.load_events()

    def create_widgets(self) -> None:
        self.title_label = QLabel("Events")
        self.title_label.setObjectName("pageTitle")
        self.description_label = QLabel("Keep track of exams, quizzes, labs and important deadlines.")
        self.description_label.setObjectName("pageDescription")
        self.empty_message = QLabel("No events yet.")
        self.empty_message.setObjectName("eventEmptyMessage")
        self.events_list = QListWidget()
        self.events_list.setObjectName("eventsList")

    def create_layout(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(30, 24, 30, 30)
        page_layout.setSpacing(18)
        page_layout.addWidget(self.title_label)
        page_layout.addWidget(self.description_label)
        page_layout.addWidget(self.empty_message, 1)
        page_layout.addWidget(self.events_list, 1)

    def load_events(self) -> None:
        self.events_list.clear()
        module_names = {module.id: module.name for module in self.module_database.get_modules()}
        for study_event in self.event_database.get_events():
            self.add_event_item(study_event, module_names)
        self.update_empty_state()

    # ------------------------------ Utilities ------------------------------

    def add_event_item(self, study_event: StudyEvent, module_names: dict[int, str]) -> None:
        item = QListWidgetItem(self.event_item_text(study_event, module_names))
        item.setData(Qt.ItemDataRole.UserRole, study_event)
        self.events_list.addItem(item)

    @staticmethod
    def event_item_text(study_event: StudyEvent, module_names: dict[int, str]) -> str:
        event_details = [study_event.event_type.value.title(), study_event.event_date.strftime("%d %b %Y")]
        if study_event.event_time is not None:
            event_details.append(study_event.event_time.strftime("%H:%M"))
        if study_event.module_id is not None:
            event_details.append(module_names[study_event.module_id])
        return f'{study_event.title}\n{" · ".join(event_details)}'

    def update_empty_state(self) -> None:
        has_events = self.events_list.count() > 0
        self.events_list.setVisible(has_events)
        self.empty_message.setVisible(not has_events)
