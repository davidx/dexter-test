from http import HTTPStatus
from flask import Flask, request, jsonify
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import os
import logging
import sqlite3
import unittest