from django.test import TestCase
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

# Create your tests here.
class ProfileListTest(APITestCase):
    def post_profile(self):
        url=reverse("profilelist")
        data={
          "profile_picture":"car.jpg"
          "bio":"good"
          "contacts":"0790999999"
          "profile":"12"
        }
        response=self.client.post(url, data)
        return response

    def test_post_profile(self):
        response= self.post_profile()
        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.count()==1

    def test_get_all_profiles(self):
        profiles=Profile.objects.all()
        assert len(profiles)==1   

    def test_get_single_profile(self):
        self.post_profile()
        id_1="1"
        url_1=reverse("singleprofile",kwargs={"id":id_1})
        response_1=self.client.get(url_1)
        assert response_1.status_code == status.HTTP_200_OK

    def update_single_profile(self): 
        response= self.post_profile()
        data={"profile_picture":"car.jpg",
              "bio":"just here",
              "contacts":"0700000000",
              "profile":"12",
        }
        url_1=reverse("singleprofile","kwargs"={"pk":response.data['id']}) 
        put_response=self.client.put(url_1,data)
        assert put_response.status_code ==status.HTTP_200_OK
        assert put_response.data["profile_picture","bio","contacts","profile"]== data["profile_picture","bio","contacts","profile"]




