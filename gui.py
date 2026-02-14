import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QCheckBox, QTextEdit,
    QFileDialog, QMessageBox, QGroupBox, QTabWidget, QDoubleSpinBox,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QSettings


class U8g2FontGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("U8g2 字库生成器")
        self.setMinimumSize(800, 700)
        
        # 持久化设置
        self.settings = QSettings("U8g2FontGenerator", "Config")
        self.current_config_path = ""
        
        self.init_ui()
        self.load_last_config()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 配置文件操作区域
        config_group = QGroupBox("配置文件")
        config_layout = QHBoxLayout(config_group)
        
        self.config_path_edit = QLineEdit()
        self.config_path_edit.setPlaceholderText("选择或保存配置文件路径...")
        config_layout.addWidget(self.config_path_edit)
        
        self.btn_load_config = QPushButton("载入配置")
        self.btn_load_config.clicked.connect(self.load_config_file)
        config_layout.addWidget(self.btn_load_config)
        
        self.btn_save_config = QPushButton("保存配置")
        self.btn_save_config.clicked.connect(self.save_config_file)
        config_layout.addWidget(self.btn_save_config)
        
        main_layout.addWidget(config_group)
        
        # 字体配置区域
        font_group = QGroupBox("字体配置")
        font_layout = QVBoxLayout(font_group)
        
        # 字体名称
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("字体名称:"))
        self.font_name_edit = QLineEdit("myFont")
        row1.addWidget(self.font_name_edit)
        font_layout.addLayout(row1)
        
        # 字体文件路径
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("字体文件:"))
        self.font_path_edit = QLineEdit()
        self.font_path_edit.setPlaceholderText("选择 TTF 字体文件...")
        row2.addWidget(self.font_path_edit)
        self.btn_browse_font = QPushButton("浏览...")
        self.btn_browse_font.clicked.connect(self.browse_font_file)
        row2.addWidget(self.btn_browse_font)
        font_layout.addLayout(row2)
        
        # DPI 和大小
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("字体 DPI:"))
        self.font_dpi_spin = QSpinBox()
        self.font_dpi_spin.setRange(1, 1000)
        self.font_dpi_spin.setValue(72)
        row3.addWidget(self.font_dpi_spin)
        
        row3.addWidget(QLabel("字体大小 (px):"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(1, 1000)
        self.font_size_spin.setValue(16)
        row3.addWidget(self.font_size_spin)
        
        row3.addWidget(QLabel("字间距 (%)"))
        self.font_spacing_spin = QSpinBox()
        self.font_spacing_spin.setRange(0, 500)
        self.font_spacing_spin.setValue(100)
        row3.addWidget(self.font_spacing_spin)
        
        row3.addStretch()
        font_layout.addLayout(row3)
        
        # 选项
        row4 = QHBoxLayout()
        self.filter_ascii_check = QCheckBox("过滤 ASCII 字符")
        self.filter_ascii_check.setChecked(True)
        row4.addWidget(self.filter_ascii_check)
        
        self.map_include_ascii_check = QCheckBox("MAP 包含 ASCII")
        row4.addWidget(self.map_include_ascii_check)
        
        row4.addStretch()
        font_layout.addLayout(row4)
        
        main_layout.addWidget(font_group)
        
        # 输出配置
        output_group = QGroupBox("输出配置")
        output_layout = QHBoxLayout(output_group)
        
        output_layout.addWidget(QLabel("输出目录:"))
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("选择输出目录...")
        output_layout.addWidget(self.output_dir_edit)
        
        self.btn_browse_output = QPushButton("浏览...")
        self.btn_browse_output.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.btn_browse_output)
        
        main_layout.addWidget(output_group)
        
        # 字符源配置（Tab 切换）
        source_group = QGroupBox("字符源配置")
        source_layout = QVBoxLayout(source_group)
        
        self.source_tabs = QTabWidget()
        
        # Tab 1: 从代码文件提取
        self.files_tab = QWidget()
        files_layout = QVBoxLayout(self.files_tab)
        
        files_btn_layout = QHBoxLayout()
        self.btn_add_files = QPushButton("添加文件")
        self.btn_add_files.clicked.connect(self.add_source_files)
        files_btn_layout.addWidget(self.btn_add_files)
        
        self.btn_add_dir = QPushButton("添加目录")
        self.btn_add_dir.clicked.connect(self.add_source_dir)
        files_btn_layout.addWidget(self.btn_add_dir)
        
        self.btn_remove_file = QPushButton("移除选中")
        self.btn_remove_file.clicked.connect(self.remove_source_file)
        files_btn_layout.addWidget(self.btn_remove_file)
        
        self.btn_clear_files = QPushButton("清空")
        self.btn_clear_files.clicked.connect(self.clear_source_files)
        files_btn_layout.addWidget(self.btn_clear_files)
        
        files_btn_layout.addStretch()
        files_layout.addLayout(files_btn_layout)
        
        self.file_list = QListWidget()
        files_layout.addWidget(self.file_list)
        
        self.source_tabs.addTab(self.files_tab, "从代码文件提取")
        
        # Tab 2: 自定义字符
        self.custom_tab = QWidget()
        custom_layout = QVBoxLayout(self.custom_tab)
        
        custom_layout.addWidget(QLabel("输入自定义字符（将直接用于生成字库）:"))
        self.custom_chars_edit = QTextEdit()
        self.custom_chars_edit.setPlaceholderText("在此输入需要生成字库的字符，例如：你好世界123...")
        self.custom_chars_edit.setMaximumHeight(150)
        custom_layout.addWidget(self.custom_chars_edit)
        
        self.source_tabs.addTab(self.custom_tab, "自定义字符")
        
        source_layout.addWidget(self.source_tabs)
        main_layout.addWidget(source_group)
        
        # 生成按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_generate = QPushButton("生成字库")
        self.btn_generate.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_generate.clicked.connect(self.generate_font)
        btn_layout.addWidget(self.btn_generate)
        
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
        # 日志输出
        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(150)
        log_layout.addWidget(self.log_edit)
        
        main_layout.addWidget(log_group)
    
    def browse_font_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择字体文件", "", "字体文件 (*.ttf *.otf);;所有文件 (*.*)"
        )
        if file_path:
            self.font_path_edit.setText(file_path)
    
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def add_source_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择源代码文件", "", "C/C++ 文件 (*.c *.cpp *.h *.hpp);;所有文件 (*.*)"
        )
        for path in file_paths:
            if not self.file_list.findItems(path, Qt.MatchExactly):
                self.file_list.addItem(path)
    
    def add_source_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择源代码目录")
        if dir_path:
            # 添加目录通配符模式
            pattern = os.path.join(dir_path, "*")
            if not self.file_list.findItems(pattern, Qt.MatchExactly):
                self.file_list.addItem(pattern)
    
    def remove_source_file(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
    
    def clear_source_files(self):
        self.file_list.clear()
    
    def load_config_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择配置文件", "", "JSON 文件 (*.json);;所有文件 (*.*)"
        )
        if file_path:
            self.load_config_from_path(file_path)
    
    def load_config_from_path(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 应用配置到界面
            self.font_name_edit.setText(config.get('font_name', 'myFont'))
            self.font_path_edit.setText(config.get('font_path', ''))
            self.font_dpi_spin.setValue(config.get('font_dpi', 72))
            self.font_size_spin.setValue(config.get('font_size_px', 16))
            self.font_spacing_spin.setValue(config.get('font_spacing_percent', 100))
            self.filter_ascii_check.setChecked(config.get('filter_ascii', True))
            self.map_include_ascii_check.setChecked(config.get('map_include_ascii', False))
            self.output_dir_edit.setText(config.get('output_dir', ''))
            
            # 清空并重新填充文件列表
            self.file_list.clear()
            self.custom_chars_edit.clear()
            
            if 'custom_chars' in config:
                self.custom_chars_edit.setPlainText(config['custom_chars'])
                self.source_tabs.setCurrentIndex(1)  # 切换到自定义字符标签
            elif 'file_paths' in config:
                for path in config['file_paths']:
                    self.file_list.addItem(path)
                self.source_tabs.setCurrentIndex(0)  # 切换到文件列表标签
            
            self.config_path_edit.setText(file_path)
            self.current_config_path = file_path
            
            # 保存最后使用的配置路径
            self.settings.setValue("last_config_path", file_path)
            
            self.log(f"已加载配置: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置文件失败:\n{str(e)}")
    
    def save_config_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存配置文件", "", "JSON 文件 (*.json);;所有文件 (*.*)"
        )
        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            config = self.get_config_from_ui()
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                self.config_path_edit.setText(file_path)
                self.current_config_path = file_path
                self.settings.setValue("last_config_path", file_path)
                
                self.log(f"配置已保存: {file_path}")
                QMessageBox.information(self, "成功", "配置文件已保存！")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存配置文件失败:\n{str(e)}")
    
    def get_config_from_ui(self):
        """从界面获取配置数据"""
        config = {
            'font_name': self.font_name_edit.text(),
            'font_path': self.font_path_edit.text(),
            'font_dpi': self.font_dpi_spin.value(),
            'font_size_px': self.font_size_spin.value(),
            'font_spacing_percent': self.font_spacing_spin.value(),
            'filter_ascii': self.filter_ascii_check.isChecked(),
            'map_include_ascii': self.map_include_ascii_check.isChecked(),
            'output_dir': self.output_dir_edit.text()
        }
        
        # 根据当前选中的标签页决定字符源
        if self.source_tabs.currentIndex() == 1:
            # 自定义字符模式
            custom_chars = self.custom_chars_edit.toPlainText()
            if custom_chars:
                config['custom_chars'] = custom_chars
        else:
            # 文件列表模式
            file_paths = []
            for i in range(self.file_list.count()):
                file_paths.append(self.file_list.item(i).text())
            if file_paths:
                config['file_paths'] = file_paths
        
        return config
    
    def load_last_config(self):
        """加载上次使用的配置文件"""
        last_path = self.settings.value("last_config_path", "")
        if last_path and os.path.exists(last_path):
            self.load_config_from_path(last_path)
    
    def generate_font(self):
        """生成字库"""
        config = self.get_config_from_ui()
        
        # 验证配置
        if not config.get('font_name'):
            QMessageBox.warning(self, "警告", "请输入字体名称！")
            return
        
        if not config.get('font_path') or not os.path.exists(config['font_path']):
            QMessageBox.warning(self, "警告", "请选择有效的字体文件！")
            return
        
        if 'custom_chars' not in config and 'file_paths' not in config:
            QMessageBox.warning(self, "警告", "请配置字符源（代码文件或自定义字符）！")
            return
        
        # 保存临时配置文件
        temp_config_path = os.path.join(os.path.dirname(__file__), "temp_config.json")
        try:
            with open(temp_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存临时配置失败:\n{str(e)}")
            return
        
        # 运行 main.py
        self.log("开始生成字库...")
        self.btn_generate.setEnabled(False)
        
        try:
            main_script = os.path.join(os.path.dirname(__file__), "main.py")
            
            # 使用当前 Python 解释器运行
            result = subprocess.run(
                [sys.executable, main_script, temp_config_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            # 输出日志
            if result.stdout:
                self.log(result.stdout)
            if result.stderr:
                self.log(result.stderr)
            
            if result.returncode == 0:
                self.log("字库生成成功！")
                QMessageBox.information(self, "成功", "字库生成成功！")
                
                # 打开输出目录
                output_dir = config.get('output_dir', '')
                if output_dir and os.path.exists(output_dir):
                    os.startfile(output_dir)
                else:
                    os.startfile(os.path.dirname(__file__))
            else:
                self.log(f"生成失败，返回码: {result.returncode}")
                QMessageBox.critical(self, "错误", "字库生成失败，请查看日志！")
                
        except Exception as e:
            self.log(f"运行错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"运行生成脚本失败:\n{str(e)}")
        finally:
            self.btn_generate.setEnabled(True)
            # 清理临时配置文件
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
    
    def log(self, message):
        """添加日志"""
        self.log_edit.append(message)


def main():
    app = QApplication(sys.argv)
    window = U8g2FontGenerator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
