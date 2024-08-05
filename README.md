# 2020년 박스오피스 영화데이터 조회

## 목차
- [소개](#소개)
- [기능](#기능)
- [기능 상세사항](#기능-상세사항)
- [기능 패키지](#기능-패키지)
- [사용법](#사용법)
- [Contribution](#Contribution)
- [라이선스](#라이선스)
- [문의](#문의)


## 소개
"2020년 박스오피스 영화 데이터 조회" 프로젝트는 2020년 동안 개봉된 영화들의 박스오피스 데이터를 수집하고 조회할 수 있는 애플리케이션입니다. 이 프로젝트는 영화 산업 분석가, 영화 팬, 마케터, 연구자들이 2020년 박스오피스 트렌드를 쉽게 파악하고 분석할 수 있도록 돕기 위해 만들어졌습니다.

주요 사용 사례는 다음과 같습니다.
- 2020년 박스오피스 순위 조회
- 특정 영화 상영횟수, 관객수, 누적관객수 조회
- 특정 영화의 수익 데이터 조회
- 월별, 일별 박스오피스 트렌드 분석
- 박스오피스 데이터 시각화(IN PROGRESS)

이 프로젝트를 통해 사용자는 2020년 동안 영화 산업이 어떻게 변화했는지, 이를 기반으로 다양한 분석과 연구를 수행할 수 있습니다.

## 기능
- 기능 1: 2020년 박스오피스 영화 데이터 수집(Extract)
- 기능 2: 2020년 박스오피스 영화 데이터 가공(Transform)
- 기능 3: 2020년 박스오피스 영화 데이터 저장(Load)

### 기능 상세사항
- 기능 1: 영화 데이터 수집은 [영화진흥위원회 오픈 API 소스](https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do)를 이용
- 기능 2: 수집된 영화 데이터의 데이터타입 변환 및 월별 트렌드 분석을 위한 컬럼 추가, 누적관객수 내림차순 정렬 
```python
#'load_dt'는 일자를 의미합니다.
df['month'] = pd.to_datetime(df['load_dt']).dt.month
    df[['rank', 'showCnt', 'audiCnt', 'salesAmt', 'audiAcc', 'salesAcc', 'salesShare']] = df[['rank', 'showCnt', 'audiCnt', 'salesAmt', 'audiAcc', 'salesAcc', 'salesShare']].astype(float).astype(int)
    df = df.sort_values(by='audiCnt', ascending=False)
```
- 기능 3: 가공된 영화 데이터 월별/일별 parquet 파일을 "~/code/playgogo/storage"에 저장
```python
df.to_parquet("~/code/playgogo/storage", partition_cols=['month','load_dt'])
```

### 기능 패키지
- 각 기능에는 특정한 의존성(dependencies)이 필요합니다. 다음은 기능별로 필요한 패키지와 설치 방법에 대한 설명입니다.

기능 1: 영화 데이터 수집
- 의존성 패키지: `requests` , `pandas`
- 설치방법:
```bash
$ pip install requests
```
```bash
$ pip install pandas
```
`requests`는 영화진흥위원회 오픈 API를 사용하여 영화 데이터를 수집합니다. API에 요청을 보내고 데이터를 수신합니다.
`pandas`는 수집한 데이터를 DataFrame 형태로 변환해줍니다.

기능 2: 데이터 변환 및 분석
- 의존성 패키지: [Extrct 패키지](https://github.com/play-gogo/Extract/releases/tag/day2)
- 설치방법:
```bash
$ pip install git+https://github.com/play-gogo/Extract.git@d2/0.1.0
$ pdm add git+https://github.com/play-gogo/Extract.git@d2/0.1.0
```
`Extrct`는 영화진흥위원회(KOFIC) API를 사용하여 박스오피스 데이터를 가져오고 이를 Pandas 데이터프레임으로 변환하는 작업을 수행합니다. 

기능 3: 데이터 저장
- 의존성 패키지: [Transform 패키지](https://github.com/play-gogo/transform/releases/tag/day2), `pyarrow`
- 설치방법:
```bash
$ pip install git+https://github.com/play-gogo/transform.git@d2.0.0/test
$ pdm add git+https://github.com/play-gogo/transform.git@d2.0.0/test
```
```bash
$ pip install pyarrow
$ pdm add pyarrow
```
`Transform`은 변환된 데이터타입과 월별로 확인할 수 있는 Month 컬럼이 추가된 데이터프레임을 제공합니다.
가공된 데이터를 Parquet 파일 형식으로 저장하기 위해 pandas와 pyarrow 패키지를 사용합니다. 데이터는 월별 및 일별로 분할되어 지정된 경로에 저장됩니다.


이와 같은 패키지 설치 과정을 통해 모든 기능을 정상적으로 사용할 수 있습니다. 필요한 패키지를 설치한 후 각 기능을 구현하는 코드를 실행하여 영화 데이터를 수집, 변환, 분석, 저장할 수 있습니다.

## 사용법
- 해당 애플리케이션을 사용하기 위해서는 Apache Airflow가 설치되어 있어야 합니다.

에어플로우 설치
[설치에 관한 공식문서 바로가기](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
에어플로우가 이미 설치되어 있다면 이 단계는 넘어갑니다.

에어플로우 dags 파일 Git clone
```bash
$ git clone https://github.com/play-gogo/airflow_dags.git
```

에어플로우 실행
```bash
$ airflow standalone
```
그런 다음 브라우저에서 http://localhost:8080으로 이동합니다.
admin 암호 확인은 다음을 입력하여 확인합니다.
```bash
$ cat ~/airflow/standalone_admin_password.txt
```
'movie' dag를 Activate 하고 실행합니다.

파일 확인
```bash
$ cd ~/code/playgogo/storage
```
저장된 영화 데이터를 확인합니다.

## Contribution
play-gogo는 Contributor를 언제나 환영합니다. Contribution을 원하시면 다음 단계를 따라주세요:

1. 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다 (git checkout -b new-feature).
3. 변경 사항을 커밋합니다 (git commit -am 'Add some feature').
4. 브랜치에 푸시합니다 (git push origin new-feature).
5. 새로운 풀 리퀘스트를 생성합니다.
6. 변경 사항에 따라 테스트 업데이트는 필수입니다.

## 라이선스
이 프로젝트는 play-gogo 라이선스에 따라 라이선스가 부과됩니다.

## 문의
질문이나 제안사항이 있으면 언제든지 연락주세요:
- 이메일: play-gogo@play-gogo.com
- GitHub: hun0219, sooj1n, hamsunwoo








