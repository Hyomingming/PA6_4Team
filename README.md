# PA6_4Team
본 프로젝트는 아두이노 센서와 라즈베리파이 센서들을 활용해서 IoT Client & IoT Server를 구현하기 위해 만들어졌다.

교수님이 수업때 설명해주신 파일을 바탕으로 코딩하였으며, 기기는 아두이노 Ultrasonic sensor와 라즈베리파이 RGB 및 Buzzer actuator를 활용하였다.

서버에 접속한 클라이언트는 IoTClient 클래스의 run() 함수를 실행시키면서, sen_data() 함수로부터 실시간으로 데이터를 입력받는다.

라즈베리파이는 serialFromArduino.readline() 함수가 수행됨에 따라서 아두이노로부터 실시간으로 초음파값을 읽어오게 된다.

받아온 초음파값을 바탕으로 if-elif 구문을 실행하면, 현재 초음파의 거리에 따라 'Red', 'Green', 'Blue'의 색과 Buzzer를 출력하도록 구현하였다.

조건문을 빠져나가기 전에 초음파 데이터는 yield로 출력되며 키-값의 딕셔너리 형태로 run() 함수의 request 변수에 들어가게 된다.

다음으로 logging.debug(request)로 distance를 출력하게 되는데 interval값을 0.1만큼 줬기 때문에 logging으로 0.1초마다 데이터를 출력하게 된다.

timeout이 발생했을 경우에 client는 아두이노 센서로부터 읽어온 초음파 데이터를 딕셔너리 형태로 저장해서 request 데이터를 만들게 된다.

딕셔너리 형태로 저장된 request 데이터는 json.dumps(request)를 통해서 파이썬 객체를 뽑아내게 되고 'UTF-8'형식의 바이트 객체로 인코딩하게 된다.

인코딩된 데이터는 self.sock.sendall(request_bytes)을 통해서 서버로 보내지게 된다. 클라이언트는 이러한 과정을 계속해서 반복하게 된다

클라이언트로부터 데이터를 전달받은 서버는 json.loads(line.decode('utf-8')) 한 줄씩 불러와서 'UTF-8'형식의 바이트 객체로 디코딩하게 된다.

그리고 status를 'OK'로 바꾸고 client와 request data를 logging.debug형식으로 출력한다.

서버로 넘어간 데이터는 딕셔너리로 저장된 distance 데이터를 불러오게 된다.

만약에 데이터가 존재할 경우 searchs.models-Search 클래스의 name과 state에 각각 distance와 초음파 데이터를 저장한다.

저장한 데이터는 .save()를 통해서 PA6_4Team/piSocket/piSocket/piSocket/settings.py의 DATABASE에 저장하게 된다.

request data를 수신한 서버는 response reply를 보내기 위해 json.dumps(response)와 response.encode('utf-8') + b'\n'로 데이터를 인코딩해서 wfile에 write한다.

timeout이 발생하지 않았을 때는 else문을 실행하여 서버로부터 response data를 얻어오게 된다.
