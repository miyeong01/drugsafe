import csv
from django.core.management.base import BaseCommand
from medicines.models import Drug, Form, Symptom

class Command(BaseCommand):
    help = 'CSV 데이터를 DB에 적재합니다.'

    def handle(self, *args, **kwargs):
        file_path = 'DrugSafe.csv' 

        print(f"[{file_path}] 데이터 적재를 시작합니다...")

        try:
            with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                count = 0
                for row in reader:
                    # (1) 제형, 증상 처리
                    form_name = row.get('제형', '').strip() or '기타'
                    form_obj, _ = Form.objects.get_or_create(name=form_name)

                    symptom_name = row.get('증상', '').strip() or '기타'
                    symptom_obj, _ = Symptom.objects.get_or_create(name=symptom_name)

                    # (2) Drug 데이터 생성 (create 사용)
                    # 주의: defaults={...}를 쓰지 않고 바로 필드명을 나열해야 합니다.
                    Drug.objects.create(
                        name=row['제품명'], 
                        company=row.get('업체명', ''),
                        basis=row.get('주성분', ''),
                        efficacy=row.get('이 약의 효능은 무엇입니까?', ''),
                        use=row.get('이 약은 어떻게 사용합니까?', ''),
                        description=row.get('이 약을 사용하기 전에 반드시 알아야 할 내용은 무엇입니가?', ''),
                        caution=row.get('이 약의 사용상 주의사항은 무엇입니까?', ''),
                        caution_intake=row.get('이 약을 사용하는 동안 주의해야 할 약 또는 음식은 무엇입니까?', ''),
                        side_effect=row.get('이 약은 어떤 이상반응이 나타날 수 있습니까?', ''),
                        store=row.get('이 약은 어떻게 보관해야 합니까?', ''),
                        
                        # ForeignKey 연결
                        form=form_obj,
                        symptom=symptom_obj,
                    )
                    
                    count += 1
                    
                    if count % 100 == 0:
                        print(f"{count}개 처리 중...")

            print("=" * 30)
            print(f"작업 완료! 총 {count}개의 데이터가 DB에 모두 저장되었습니다.")

        except FileNotFoundError:
            print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")