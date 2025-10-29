# athletes/utils.py
import json
import xml.etree.ElementTree as ET
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Athlete

class FileProcessor:
	def __init__(self):
		self.upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
		os.makedirs(self.upload_dir, exist_ok=True)

	def sanitize_filename(self, filename):
		"""Очистка имени файла"""
		import re
		name, ext = os.path.splitext(filename)
		name = re.sub(r'[^\w\s-]', '', name)
		name = re.sub(r'[-\s]+', '-', name).strip('-_')
		return f"{name}{ext}".lower()

	def is_valid_json(self, file_path):
		"""Проверка валидности JSON файла"""
		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				json.load(f)
			return True
		except (json.JSONDecodeError, UnicodeDecodeError):
			return False

	def is_valid_xml(self, file_path):
		"""Проверка валидности XML файла"""
		try:
			ET.parse(file_path)
			return True
		except ET.ParseError:
			return False

	def save_uploaded_file(self, uploaded_file):
		"""Сохранение загруженного файла"""
		filename = self.sanitize_filename(uploaded_file.name)
		file_path = os.path.join(self.upload_dir, filename)

		with open(file_path, 'wb+') as destination:
			for chunk in uploaded_file.chunks():
				destination.write(chunk)

		return file_path, filename

	def read_json_file(self, file_path):
		"""Чтение JSON файла"""
		with open(file_path, 'r', encoding='utf-8') as f:
			return json.load(f)

	def read_xml_file(self, file_path):
		"""Чтение XML файла"""
		tree = ET.parse(file_path)
		root = tree.getroot()

		data = []
		for athlete_elem in root.findall('athlete'):
			athlete_data = {}
			for child in athlete_elem:
				athlete_data[child.tag] = child.text
			data.append(athlete_data)

		return data

	def export_to_json(self, athletes_data, filename):
		"""Экспорт данных в JSON"""
		file_path = os.path.join(self.upload_dir, f"{filename}.json")
		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump(athletes_data, f, ensure_ascii=False, indent=2)
		return file_path

	def export_to_xml(self, athletes_data, filename):
		"""Экспорт данных в XML"""
		file_path = os.path.join(self.upload_dir, f"{filename}.xml")

		root = ET.Element('athletes')
		for athlete in athletes_data:
			athlete_elem = ET.SubElement(root, 'athlete')
			for key, value in athlete.items():
				child = ET.SubElement(athlete_elem, key)
				child.text = str(value)

		tree = ET.ElementTree(root)
		tree.write(file_path, encoding='utf-8', xml_declaration=True)
		return file_path

	def get_all_files(self):
		"""Получение всех JSON/XML файлов"""
		json_files = []
		xml_files = []

		for filename in os.listdir(self.upload_dir):
			if filename.endswith('.json'):
				json_files.append(filename)
			elif filename.endswith('.xml'):
				xml_files.append(filename)

		return json_files, xml_files

	def read_file_content(self, filename):
		"""Чтение содержимого файла"""
		file_path = os.path.join(self.upload_dir, filename)

		if filename.endswith('.json'):
			return self.read_json_file(file_path), 'json'
		elif filename.endswith('.xml'):
			return self.read_xml_file(file_path), 'xml'
		else:
			return None, None