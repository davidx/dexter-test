from flask import Flask, request, jsonify
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from http import HTTPStatus
import logging
import sqlite3
import unittest

app = Flask(__name__)