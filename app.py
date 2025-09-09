import streamlit as st
import datetime
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':

    st.title("ユーザー登録画面")

    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            # "user_id": user_id,
            "username": user_name
        }
        submit_button = st.form_submit_button(label='ユーザー登録')

    if submit_button:
        st.write("## 送信データ")
        st.write(("## レスポンス結果"))
        url = "http://127.0.0.1:8000/users"
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.write(res.status_code)
        st.json(res.json())


elif page == 'rooms':

    st.title("APIテスト画面（会議室）")

    with st.form(key='rooms'):
        # room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

    if submit_button:
        url = "http://127.0.0.1:8000/rooms"
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success("会議室登録完了")
        st.write(res.status_code)
        st.json(res.json())

elif page == 'bookings':

    st.title("会議室予約画面")
    # ユーザー一覧を取得
    url_users = "http://127.0.0.1:8000/users"
    res = requests.get(url_users)
    if res.status_code == 200:
        users = res.json() # JSONデータをPythonオブジェクトに変換
    else:
        users = []


    #  ユーザー名をキー、ユーザーIDをバリュー
    users_name = {user['username']: user['user_id'] for user in users}
    st.write(users_name)

    # 会議室一覧の取得
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    if res.status_code == 200:
        rooms = res.json()
        rooms_name = {}
        for room in rooms:
            rooms_name[room['room_name']] = {
                'room_id': room['room_id'],
                'capacity': room['capacity']
            }
    else:
        rooms = []

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_bookings = "http://127.0.0.1:8000/bookings"
    res = requests.get(url_bookings)
    if res.status_code == 200:
        bookings = res.json() # JSONデータをPythonオブジェクトに変換
        df_bookings = pd.DataFrame(bookings) # パンダスのデータ型に変換
        st.write('### 予約一覧')
        st.table(df_bookings)

        users_id = {}
        for user in users:
            users_id[user['user_id']] = user['username']
        
        rooms_id = {}
        for room in rooms:
            rooms_id[room['room_id']] = {
                'room_name': room['room_name'], # IDをキーにして部屋の名前を取得
                'capacity': room['capacity'],
            }


        # IDを各値に変更

        

    with st.form(key='bookings'):
        username: str = st.selectbox('予約者名', users_name.keys())
        room_name: str = st.selectbox('予約者名', rooms_name.keys())
        booked_num: int = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('日付を入力', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻', value=datetime.time(hour=20, minute=0))
        
       
        submit_button = st.form_submit_button(label='予約登録')

    if submit_button:
        user_id: int = users_name[username]
        room_id: int = rooms_name[room_name]['room_id']
        capacity: int = rooms_name[room_name]['capacity']


        data = {
            'user_id': user_id,
            'room_id': room_id,
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        # 定員以下の予約人数の場合
        if booked_num <= capacity:
            # 会議室の予約
            url = "http://127.0.0.1:8000/bookings"
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            st.write(res.status_code)
            if res.status_code == 200:
                st.success("予約登録完了")
            st.json(res.json())
        else:
            st.error(f'{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみ受け付けております。')