from rest_framework import status
from rest_framework.test import APITestCase
from .models import InterventionRecord
from django.urls import reverse


# Create your tests here.
class InteventionRecordTests(APITestCase):
    def post_intervention_record(self):
        url = reverse("create-intervention-item")
        data = {
            "title" : "no power",
            "description" : "poor connection of power lines",
            "location"  : "ruiru"
        }
        response = self.client.post(url, data)
        return response
    
    def test_post_intervention_record(self):
        response = self.post_intervention_record()
        assert response.status_code == status.HTTP_201_CREATED
        assert InterventionRecord.objects.count() == 1

    def test_filter_intervention_record_by_title(self):
        self.post_intervention_record()
        title_1 = "power"
        url_1 = reverse("fetch-intervention-records", kwargs={"title": title_1})
        response_2 = self.client.get(url_1 )
        assert response_2.status_code == status.HTTP_200_OK
        title_2 = "sewage"
        url_2 = reverse("fetch-intervention-records", kwargs={"title": title_2})
        response_3 = self.client.get(url_2)
        assert response_3.status_code == status.HTTP_404_NOT_FOUND

    def test_intervention_record_detail(self):
        response_1 = self.post_intervention_record()
        url_1 = reverse("intervention-detail", kwargs={"pk": response_1.data["id"]})
        response_2 = self.client.get(url_1, format ="json")
        assert response_2.status_code == status.HTTP_200_OK
        url_2 = reverse("intervention-detail", kwargs={"pk": 100})
        response_3 = self.client.get(url_2, format ="json")
        assert response_3.status_code == status.HTTP_404_NOT_FOUND

    def test_update_intervention_record_detail(self):
        response = self.post_intervention_record()
        data = {"title" : "power outage"}
        url_1 = reverse("intervention-detail", kwargs={"pk": response.data["id"]})
        put_response= self.client.put(url_1, data)
        assert put_response.status_code  == status.HTTP_200_OK
        assert put_response.data["title"]  == data["title"]
        put_response_2 = self.client.put(url_1)
        assert put_response_2.status_code == status.HTTP_400_BAD_REQUEST
        url_2 = reverse("intervention-detail", kwargs={"pk": 100})
        put_response_3= self.client.put(url_2)
        assert put_response_3.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_intervention_record_detail(self):
        response_1 = self.post_intervention_record()
        url_1 = reverse("intervention-detail", kwargs={"pk" : response_1.data["id"]})
        response_2 = self.client.delete(url_1)
        assert response_2.status_code == status.HTTP_204_NO_CONTENT
        response_3 = self.client.delete(url_1)
        assert response_3.status_code == status.HTTP_404_NOT_FOUND

    def test_filter_intervention_record_by_status(self):
        response_1 = self.post_intervention_record()
        data = {
            "title" : response_1.data["title"],
            "status" : "resolved",
        }
        url_1 = reverse("intervention-detail", kwargs={"pk" : response_1.data["id"]})
        self.client.put(url_1, data)
        url_2 = reverse("filter-by-status" ,kwargs={"intervention_status" : data["status"]})
        response_2 = self.client.get(url_2)
        assert response_2.status_code == status.HTTP_200_OK
        assert InterventionRecord.objects.count() == 1
        url_3 = reverse("filter-by-status", kwargs={"intervention_status" : "none"})
        response_3 =self.client.get(url_3)
        assert response_3.status_code == status.HTTP_404_NOT_FOUND
