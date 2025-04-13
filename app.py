    def test_add_user_success(self):
        # Mock the ScyllaDB session and successful user insertion
        with unittest.mock.patch('cassandra.cluster.Cluster') as mock_cluster:
            mock_session = mock_cluster.return_value.connect.return_value
            mock_session.execute.return_value = None

            user_data = {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com'
            }
            response = self.app.post('/add_user', json=user_data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), {'message': 'User added successfully'})