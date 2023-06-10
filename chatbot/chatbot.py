import pandas as pd #CSV 파일을 읽을 판다스 라이브러리를 pd로 가져오기

class LDChatBot: #LDChatBot 클래스 정의
    def __init__(sampledata, chatbotdata): #LDChatBot 클래스의 인스턴스가 생성될 때 호출됨. sampledata는 학습 데이터 경로 & chatbotdata는 챗봇에 필요한 학습 데이터 이름
        sampledata.questions, sampledata.answers = sampledata.load_data(chatbotdata) #load_data 메서드를 호출해서 sampledata에서 질문과 답변을 로드합니다.

    def load_data(sampledata, chatbotdata): #CSV 파일에서 데이터를 로드하는 메서드
        data = pd.read_csv(chatbotdata) #pandas로 CSV 파일을 읽고,
        questions = data['Q'].tolist() #학습파일 안에 있는 질문 열에서 질문을 추출하고 리스트로 변환
        answers = data['A'].tolist() #학습파일 안에 있는 답변 열에서 답변을 추출하고 리스트로 변환
        return questions, answers #질문과 답변 튜플을 반환

    def calc_distance(data, a, b): #레벤슈타인 거리 계산 메서드
        if a == b: return 0 #두 문자열이 같으면 거리는 0
        a_len = len(a) #a 문자열의 길이
        b_len = len(b) #b 문자열의 길이
        if a == "": return b_len #a 문자열이 비어 있으면 거리는 b 문자열의 길이
        if b == "": return a_len #b 문자열이 비어 있으면 거리는 a 문자열의 길이
        matrix = [[] for i in range(a_len+1)] #a_len+1 행의 빈 행렬 생성
        for i in range(a_len+1): #각 행에 대해
            matrix[i] = [0 for j in range(b_len+1)] #b_len+1 열의 0으로 채워진 행을 추가합
        for i in range(a_len+1): #각 행에 대해
            matrix[i][0] = i #첫 번째 열의 값을 i로 설정
        for j in range(b_len+1): #각 열에 대해
            matrix[0][j] = j #첫 번째 행의 값을 j로 설정
        for i in range(1, a_len+1): #각 문자에 대해
            ac = a[i-1] #a 문자열의 i-1번째 문자
            for j in range(1, b_len+1): #각 문자에 대해
                bc = b[j-1] #b 문자열의 j-1번째 문자
                cost = 0 if (ac == bc) else 1 #ac와 bc가 같으면 비용은 0, 아니면 1
                matrix[i][j] = min([ #matrix[i][j]의 값을 다음 중 최소값으로 설정
                    matrix[i-1][j] + 1, #위쪽 셀에서 아래로 이동하는 경우
                    matrix[i][j-1] + 1, #왼쪽 셀에서 오른쪽으로 이동하는 경우
                    matrix[i-1][j-1] + cost #대각선 셀에서 대각선으로 이동하는 경우
                ])
        return matrix[a_len][b_len] #matrix[a_len][b_len]의 값 반환

    def find_best_answer(sampledata, input_sentence): #주어진 입력 문장에 대한 가장 일치하는 답변을 찾는 메서드
        distances = [sampledata.calc_distance(input_sentence, question) for question in sampledata.questions] #입력 문장과 각 질문 사이의 거리를 계산하여 리스트에 저장
        best_match_index = distances.index(min(distances)) #distances 리스트에서 가장 작은 거리의 인덱스를 찾음
        return sampledata.answers[best_match_index] #가장 일치하는 질문에 해당하는 답변을 반환


chatbotdata = 'ChatbotData.csv'# 학습시킬 '데이터' 경로 지정

chatbot = LDChatBot(chatbotdata)    # 챗봇 객체 생성


while True: #반복문
    input_sentence = input('You: ') #'You'가 입력한 내용이 input_sentence 변수에 저장되는데, 이때 'You'가 입력한 내용이
    if input_sentence.lower() == '종료': #'종료'이면
        break #반복문을 종료하고, 
    response = chatbot.find_best_answer(input_sentence) #아니면, find_best_answer 메서드를 사용하여 사용자가 입력한 문장에서 가장 적합한 답변 찾아 chatbot 객체의 response에 넣어줌
    print('Chatbot:', response) #'Chatbot'의 response 변수값를 출력