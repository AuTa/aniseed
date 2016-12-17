# coding: utf-8

import unittest
from app.models import Kana, PronunciationOfKanamoji
from app import create_app
from database import SQLALCHEMY
from flask import current_app


class KanaModelTestCase(unittest.TestCase):
    def setUp(self):
        self.db = SQLALCHEMY('testing')
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()

    def test_pronun(self):
        PronunciationOfKanamoji.insert_pronunciations(self.db)
        with self.db.session as session:
            pronun = PronunciationOfKanamoji.query(session) \
                .filter_by(character='Seion').first()
        self.assertTrue(pronun is not None)

    def test_kana(self):
        PronunciationOfKanamoji.insert_pronunciations(self.db)
        Kana.insert_kanas(self.db)
        with self.db.session as session:
            kana = Kana.query(session).filter_by(romaji='a').first()
            self.assertTrue(kana.hiragana == 'あ')
            character = PronunciationOfKanamoji.query(session) \
                .filter_by(id=kana.pronunciation_id) \
                .first().character
            self.assertTrue(character == 'Seion')
