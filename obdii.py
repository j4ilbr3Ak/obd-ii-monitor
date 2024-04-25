import sys
from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QPainter, QColor, QFont
from PySide2.QtCore import Qt, QRectF, QTimer
import obd
import math

class CarDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag Racer Dashboard")
        layout = QVBoxLayout()

        # Create a list to hold pairs of gauge layouts
        gauge_layouts = []

        # RPM Gauge
        rpm_layout = QVBoxLayout()
        rpm_label = QLabel("RPM:")
        rpm_layout.addWidget(rpm_label)
        self.rpm_gauge = CustomGauge()
        rpm_layout.addWidget(self.rpm_gauge)
        gauge_layouts.append(rpm_layout)

        # Speedometer
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Speed (km/h):")
        speed_layout.addWidget(speed_label)
        self.speed_gauge = CustomGauge()
        speed_layout.addWidget(self.speed_gauge)
        gauge_layouts.append(speed_layout)

        # Coolant Temperature
        coolant_layout = QVBoxLayout()
        coolant_label = QLabel("Coolant Temp (°C):")
        coolant_layout.addWidget(coolant_label)
        self.coolant_gauge = CustomGauge()
        coolant_layout.addWidget(self.coolant_gauge)
        gauge_layouts.append(coolant_layout)

        # Intake Air Temperature
        intake_air_layout = QVBoxLayout()
        intake_air_label = QLabel("Intake Air Temp (°C):")
        intake_air_layout.addWidget(intake_air_label)
        self.intake_air_gauge = CustomGauge()
        intake_air_layout.addWidget(self.intake_air_gauge)
        gauge_layouts.append(intake_air_layout)

        # Throttle Position
        throttle_layout = QVBoxLayout()
        throttle_label = QLabel("Throttle Position (%):")
        throttle_layout.addWidget(throttle_label)
        self.throttle_gauge = CustomGauge()
        throttle_layout.addWidget(self.throttle_gauge)
        gauge_layouts.append(throttle_layout)

        # Intake Manifold Pressure
        intake_layout = QVBoxLayout()
        intake_label = QLabel("Intake Manifold Pressure (kPa):")
        intake_layout.addWidget(intake_label)
        self.intake_gauge = CustomGauge()
        intake_layout.addWidget(self.intake_gauge)
        gauge_layouts.append(intake_layout)

        # Fuel Level
        fuel_layout = QVBoxLayout()
        fuel_label = QLabel("Fuel Level (%):")
        fuel_layout.addWidget(fuel_label)
        self.fuel_gauge = CustomGauge()
        fuel_layout.addWidget(self.fuel_gauge)
        gauge_layouts.append(fuel_layout)

        # Timing Advance
        timing_layout = QVBoxLayout()
        timing_label = QLabel("Timing Advance (°):")
        timing_layout.addWidget(timing_label)
        self.timing_gauge = CustomGauge()
        timing_layout.addWidget(self.timing_gauge)
        gauge_layouts.append(timing_layout)

        # Create pairs of gauges and add them to the main layout
        for i in range(0, len(gauge_layouts), 2):
            pair_layout = QHBoxLayout()
            pair_layout.addLayout(gauge_layouts[i])
            if i + 1 < len(gauge_layouts):
                pair_layout.addLayout(gauge_layouts[i + 1])
            layout.addLayout(pair_layout)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_car)
        layout.addWidget(self.connect_button)

        # Connection Status
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.connection_status)

        # Set Layout
        self.setLayout(layout)
        self.obd_connection = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gauges)

    def connect_to_car(self):
        try:
            self.obd_connection = obd.OBD()  # Connect to the car's OBD system
            self.connection_status.setText("Connected to OBD")
            self.timer.start(1000)  # Update every second
        except Exception as e:
            self.connection_status.setText(f"Error: {e}")

    def update_gauges(self):
        if self.obd_connection:
            rpm_resp = self.obd_connection.query(obd.commands.RPM)
            speed_resp = self.obd_connection.query(obd.commands.SPEED)
            coolant_resp = self.obd_connection.query(obd.commands.COOLANT_TEMP)
            intake_air_resp = self.obd_connection.query(obd.commands.INTAKE_TEMP)
            throttle_resp = self.obd_connection.query(obd.commands.THROTTLE_POS)
            intake_resp = self.obd_connection.query(obd.commands.INTAKE_PRESSURE)
            fuel_resp = self.obd_connection.query(obd.commands.FUEL_LEVEL)
            timing_resp = self.obd_connection.query(obd.commands.TIMING_ADVANCE)

            if all([rpm_resp, speed_resp, coolant_resp, intake_air_resp, throttle_resp, intake_resp, fuel_resp, timing_resp]):
                rpm = rpm_resp.value.magnitude
                speed = speed_resp.value.magnitude
                coolant = coolant_resp.value.magnitude
                intake_air = intake_air_resp.value.magnitude
                throttle = throttle_resp.value.magnitude
                intake = intake_resp.value.magnitude
                fuel = fuel_resp.value.magnitude
                timing = timing_resp.value.magnitude

                self.rpm_gauge.setValue(rpm)
                self.speed_gauge.setValue(speed)
                self.coolant_gauge.setValue(coolant)
                self.intake_air_gauge.setValue(intake_air)
                self.throttle_gauge.setValue(throttle)
                self.intake_gauge.setValue(intake)
                self.fuel_gauge.setValue(fuel)
                self.timing_gauge.setValue(timing)

class CustomGauge(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 150)
        self.value = 0

    def setValue(self, value):
        self.value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define colors
        bg_color = QColor(30, 30, 30)
        fg_color = QColor(0, 255, 0)

        # Draw background
        painter.fillRect(event.rect(), bg_color)

        # Define parameters
        rect = event.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 10
        start_angle = 225
        span_angle = 90
        value_angle = start_angle + (span_angle * self.value / 100)

        # Draw arc
        painter.setPen(QColor(100, 100, 100))
        painter.drawArc(QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2), start_angle * 16, span_angle * 16)

        # Draw value
        painter.setPen(QColor(0, 255, 0))
        painter.drawArc(QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2), start_angle * 16, value_angle * 16)

        # Draw text
        painter.setFont(QFont("Arial", 12))
        painter.drawText(event.rect(), Qt.AlignCenter, f"{self.value:.0f}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = CarDashboard()
    dashboard.show()
    sys.exit(app.exec_())