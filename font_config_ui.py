import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QCheckBox, QSpinBox, 
                             QLabel, QFileDialog, QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt

class FontConfigUI(QWidget):
    def __init__(self):
        super().__init__()
        self.last_config_path = self.load_last_config_path()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('u8g2 Font Configurator')
        self.setGeometry(100, 100, 600, 500)
        
        main_layout = QVBoxLayout()
        
        # 配置文件操作区域
        file_layout = QHBoxLayout()
        self.config_path_edit = QLineEdit()
        self.config_path_edit.setPlaceholderText('配置文件路径')
        browse_btn = QPushButton('浏览')
        browse_btn.clicked.connect(self.browse_config)
        load_btn = QPushButton('载入')
        load_btn.clicked.connect(self.load_config)
        save_btn = QPushButton('保存')
        save_btn.clicked.connect(self.save_config)
        
        file_layout.addWidget(QLabel('配置文件:'))
        file_layout.addWidget(self.config_path_edit)
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(load_btn)
        file_layout.addWidget(save_btn)
        main_layout.addLayout(file_layout)
        
        # 字体配置组
        font_group = QGroupBox('字体配置')
        font_layout = QVBoxLayout()
        
        # 字体名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel('字体名称:'))
        self.font_name_edit = QLineEdit()
        name_layout.addWidget(self.font_name_edit)
        font_layout.addLayout(name_layout)
        
        # 字体路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel('字体路径:'))
        self.font_path_edit = QLineEdit()
        font_browse_btn = QPushButton('浏览')
        font_browse_btn.clicked.connect(self.browse_font)
        path_layout.addWidget(self.font_path_edit)
        path_layout.addWidget(font_browse_btn)
        font_layout.addLayout(path_layout)
        
        # 字体DPI
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel('字体DPI:'))
        self.font_dpi_spin = QSpinBox()
        self.font_dpi_spin.setRange(1, 300)
        self.font_dpi_spin.setValue(72)
        dpi_layout.addWidget(self.font_dpi_spin)
        font_layout.addLayout(dpi_layout)
        
        # 字体大小
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel('字体大小(px):'))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(1, 100)
        self.font_size_spin.setValue(16)
        size_layout.addWidget(self.font_size_spin)
        font_layout.addLayout(size_layout)
        
        # 字体间距
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel('字体间距(%):'))
        self.font_spacing_spin = QSpinBox()
        self.font_spacing_spin.setRange(1, 200)
        self.font_spacing_spin.setValue(100)
        spacing_layout.addWidget(self.font_spacing_spin)
        font_layout.addLayout(spacing_layout)
        
        # 过滤ASCII
        filter_layout = QHBoxLayout()
        self.filter_ascii_check = QCheckBox('过滤ASCII')
        self.filter_ascii_check.setChecked(True)
        filter_layout.addWidget(self.filter_ascii_check)
        font_layout.addLayout(filter_layout)
        
        # 包含ASCII映射
        map_layout = QHBoxLayout()
        self.map_include_check = QCheckBox('包含ASCII映射')
        map_layout.addWidget(self.map_include_check)
        font_layout.addLayout(map_layout)
        
        # 输出目录
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel('输出目录:'))
        self.output_dir_edit = QLineEdit()
        output_browse_btn = QPushButton('浏览')
        output_browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(output_browse_btn)
        font_layout.addLayout(output_layout)
        
        # 文件路径或自定义字符
        self.file_paths_edit = QTextEdit()
        self.file_paths_edit.setPlaceholderText('文件路径(每行一个) 或 自定义字符')
        font_layout.addWidget(QLabel('文件路径/自定义字符:'))
        font_layout.addWidget(self.file_paths_edit)
        
        font_group.setLayout(font_layout)
        main_layout.addWidget(font_group)
        
        # 生成按钮
        generate_btn = QPushButton('生成字体')
        generate_btn.clicked.connect(self.generate_font)
        main_layout.addWidget(generate_btn)
        
        self.setLayout(main_layout)
        
        # 如果有上次打开的配置文件，自动载入
        if self.last_config_path:
            self.config_path_edit.setText(self.last_config_path)
            self.load_config()
    
    def browse_config(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择配置文件', '', 'JSON Files (*.json)')
        if file_path:
            self.config_path_edit.setText(file_path)
    
    def browse_font(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择字体文件', '', 'Font Files (*.ttf *.otf)')
        if file_path:
            self.font_path_edit.setText(file_path)
    
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def load_config(self):
        config_path = self.config_path_edit.text()
        if not config_path or not os.path.exists(config_path):
            return
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.font_name_edit.setText(config.get('font_name', ''))
        self.font_path_edit.setText(config.get('font_path', ''))
        self.font_dpi_spin.setValue(config.get('font_dpi', 72))
        self.font_size_spin.setValue(config.get('font_size_px', 16))
        self.font_spacing_spin.setValue(config.get('font_spacing_percent', 100))
        self.filter_ascii_check.setChecked(config.get('filter_ascii', True))
        self.map_include_check.setChecked(config.get('map_include_ascii', False))
        self.output_dir_edit.setText(config.get('output_dir', ''))
        
        # 处理文件路径或自定义字符
        if 'file_paths' in config:
            self.file_paths_edit.setPlainText('\n'.join(config['file_paths']))
        elif 'custom_chars' in config:
            self.file_paths_edit.setPlainText(config['custom_chars'])
        
        # 保存上次打开的配置路径
        self.save_last_config_path(config_path)
    
    def save_config(self):
        config_path = self.config_path_edit.text()
        if not config_path:
            config_path, _ = QFileDialog.getSaveFileName(self, '保存配置文件', '', 'JSON Files (*.json)')
            if not config_path:
                return
        
        config = {
            'font_name': self.font_name_edit.text(),
            'font_path': self.font_path_edit.text(),
            'font_dpi': self.font_dpi_spin.value(),
            'font_size_px': self.font_size_spin.value(),
            'font_spacing_percent': self.font_spacing_spin.value(),
            'filter_ascii': self.filter_ascii_check.isChecked(),
            'map_include_ascii': self.map_include_check.isChecked(),
            'output_dir': self.output_dir_edit.text()
        }
        
        # 判断是文件路径还是自定义字符
        content = self.file_paths_edit.toPlainText().strip()
        if '\n' in content:
            config['file_paths'] = [line.strip() for line in content.split('\n') if line.strip()]
        else:
            config['custom_chars'] = content
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 保存上次打开的配置路径
        self.save_last_config_path(config_path)
    
    def generate_font(self):
        # 先保存配置
        self.save_config()
        
        # 执行生成命令
        config_path = self.config_path_edit.text()
        if not config_path:
            return
        
        # 使用main.py作为生成脚本
        import subprocess
        subprocess.run([sys.executable, 'main.py', config_path], check=True)
        
        # 打开目标目录
        output_dir = self.output_dir_edit.text()
        if output_dir and os.path.exists(output_dir):
            os.startfile(output_dir)
    
    def load_last_config_path(self):
        config_file = 'last_config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data.get('last_config_path', '')
        return ''
    
    def save_last_config_path(self, path):
        config_file = 'last_config.json'
        with open(config_file, 'w') as f:
            json.dump({'last_config_path': path}, f)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = FontConfigUI()
    ui.show()
    sys.exit(app.exec_())