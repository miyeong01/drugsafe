import requests
from django.core.management.base import BaseCommand
from medicines.models import Drug
from django.conf import settings

BASE_URL = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
SERVICE_KEY = settings.DRUG_API_KEY

class Command(BaseCommand):
    help = "의약품 이미지 OpenAPI를 호출하여 image_url을 업데이트합니다."

    def handle(self, *args, **options):
        drugs = Drug.objects.filter(image_url__isnull=True)

        print(f"이미지 없는 의약품 {drugs.count()}개 처리 시작")

        for idx, drug in enumerate(drugs, start=1):
            params = {
                "serviceKey": SERVICE_KEY,
                "itemName": drug.name,
                "type": "json"
            }

            try:
                response = requests.get(BASE_URL, params=params, timeout=5)
                data = response.json()

                items = data.get("body", {}).get("items", [])
                if not items:
                    continue

                for item in items:
                    if item.get("entpName") == drug.company:
                        image = item.get("itemImage")
                        if image:
                            drug.image_url = image
                            drug.save()
                            break

                if idx % 50 == 0:
                    print(f"{idx}개 처리 완료")

            except Exception as e:
                print(f"{drug.name} 처리 중 오류: {e}")

        print("이미지 업데이트 완료")
