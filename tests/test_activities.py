"""Tests for FastAPI Activities Management System endpoints.

All tests follow the AAA (Arrange-Act-Assert) pattern for clarity and readability.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_success_status(self, client):
        """Test that GET /activities returns 200 status code.
        
        Arrange: No setup needed, client fixture provides TestClient
        Act: Make GET request to /activities
        Assert: Verify response status is 200
        """
        # Arrange
        # Client fixture is ready to use

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_activities(self, client):
        """Test that GET /activities returns a non-empty list of activities.
        
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Verify response contains activities
        """
        # Arrange
        # Client fixture is ready to use

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_returns_correct_structure(self, client):
        """Test that activities have correct structure with required fields.
        
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        # Client fixture is ready to use

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_user_to_activity_returns_success_status(self, client):
        """Test that signing up a user returns 200 status code.
        
        Arrange: Prepare test email and activity name
        Act: Make POST request to signup endpoint
        Assert: Verify response status is 200
        """
        # Arrange
        activity_name = "Chess Club"
        test_email = "test_user_1@example.com"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_user_appears_in_participants_list(self, client):
        """Test that a signed-up user appears in the activity's participants list.
        
        Arrange: Prepare test email and activity name
        Act: Sign up user, then retrieve activities
        Assert: Verify user is in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        test_email = "test_user_2@example.com"

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert signup_response.status_code == 200
        assert test_email in activities_data[activity_name]["participants"]

    def test_signup_same_user_to_different_activities(self, client):
        """Test that a user can sign up for multiple different activities.
        
        Arrange: Prepare test email and two different activity names
        Act: Sign up user to first activity, then to second activity
        Assert: Verify both signups succeed
        """
        # Arrange
        test_email = "test_user_3@example.com"
        activity_1 = "Basketball Team"
        activity_2 = "Tennis Club"

        # Act
        response_1 = client.post(
            f"/activities/{activity_1}/signup",
            params={"email": test_email}
        )
        response_2 = client.post(
            f"/activities/{activity_2}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response_1.status_code == 200
        assert response_2.status_code == 200


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/remove endpoint."""

    def test_remove_user_from_activity_returns_success_status(self, client):
        """Test that removing a user returns 200 status code.
        
        Arrange: Prepare an activity and an existing participant
        Act: Make DELETE request to remove endpoint
        Assert: Verify response status is 200
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 200

    def test_remove_user_not_in_participants_after_removal(self, client):
        """Test that a removed user no longer appears in participants list.
        
        Arrange: Prepare an activity and an existing participant
        Act: Remove user, then retrieve activities
        Assert: Verify user is not in participants list
        """
        # Arrange
        activity_name = "Gym Class"
        existing_email = "john@mergington.edu"

        # Act
        remove_response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": existing_email}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert remove_response.status_code == 200
        assert existing_email not in activities_data[activity_name]["participants"]

    def test_remove_user_from_different_activities(self, client):
        """Test that a user can be removed from multiple different activities.
        
        Arrange: Prepare two different activities with existing participants
        Act: Remove user from first activity, then from second activity
        Assert: Verify both removals succeed
        """
        # Arrange
        activity_1 = "Basketball Team"
        activity_2 = "Drama Club"
        email_1 = "alex@mergington.edu"
        email_2 = "noah@mergington.edu"

        # Act
        response_1 = client.delete(
            f"/activities/{activity_1}/remove",
            params={"email": email_1}
        )
        response_2 = client.delete(
            f"/activities/{activity_2}/remove",
            params={"email": email_2}
        )

        # Assert
        assert response_1.status_code == 200
        assert response_2.status_code == 200
