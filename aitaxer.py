import numpy as np
import pandas as pd
import streamlit as st
import time
import plotly.express as px
#import matplotlib.pyplot as plt
import graph_plot
from PIL import Image

image_title = Image.open('H:\\Pythonprojects\\aitax\\venv\\images\\picture_title.jpg')
image_pipe  = Image.open('H:\\Pythonprojects\\aitax\\venv\\images\\pipeline_aitax.png')
image_world = Image.open('H:\\Pythonprojects\\aitax\\venv\\images\\picture_world.jpg')
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
st.header('Искусственный Интеллект для рсчета налоговых отчислений.')
st.image(image_title)

with st.sidebar:
    st.markdown(''' # Содержание:''')
    st.markdown("## [1. Актуальность тематики](#about)", unsafe_allow_html=True)
    st.markdown("## [2. Этапы разработки кейса](#pipeline)", unsafe_allow_html=True)
    st.markdown("## [3. Задача](#task)", unsafe_allow_html=True)
    st.markdown("## [4. Информация о датасете](#data)", unsafe_allow_html=True)
    st.markdown("## [5. Блок 1: Анализ выборки](#analyze)", unsafe_allow_html=True)
    st.markdown("## [6. Блок 2: Самостоятельный выбор клиентов для отправки рекламы](#student_choise)", unsafe_allow_html=True)
    st.markdown("## [7. Блок 3: Подбор стратегии с помощью ML](#ml_models)", unsafe_allow_html=True)
    st.markdown("## [8. Блок 4: Подбор стратегии, исходя из бюджета](#sreategy_budget)", unsafe_allow_html=True)

st.header('Актуальность тематики', anchor='about')
st.subheader('Кому будет полезно изучить данную работу ?')
st.write('1.Студентам управленческих специальностей. Интересующимся функционированием государственных механизмов.')
st.write('2.Студентам финансовых специальносетй. Заинтересованным в изучении финансовых потоков.')
st.write('3.Студентам других специальностей, интересующимся новыми возможностями искусственного интеллекта.')

st.header('Этапы разработки кейса', anchor='pipeline')
st.image(image_pipe,caption='Этапы проектирования кейса')
with st.expander("Общая схема"):
    st.markdown(
        '''
        \n**Этапы:**
        \n1. Создаётся среда обитания ботов. База данных EMNIST, содержащая образцы рукописных букв:
        \nСодержит 800000 картинок размером 28x28 пикселей с изображением рукописных букв. [EMNIST](https://www.nist.gov/itl/products-and-services/emnist-dataset)
        \n2. Библиотека слоев:
        \nСодержит набор слоев, используемых нейронной сетью.  [tensorflow](https://www.tensorflow.org/).
        \n3. Настройка модели:
        \nУстанавливается тип и количество слоев, а также количество нейронов в них.
        \n4. Обучение модели:
        \nВо время этого процесса нейросеть просматривает картинки и сопоставляет их с метками.
        \n5. Проверка точности:
        \nНа этом этапе программист проверяет работу сети с помощью тестовых изображений.
        \n6. Функция обработки изображения:
        \nПреобразует изображение в массив чисел, который понимает нейронная сеть.
        \n7. Загрузка изображения:
        \nНа выбор студенту предлагается два варианта ввода. Первый - ввести данные с помощью камеры, второй - воспользоваться заранее отобранными изображениями.
        \n8. Проверка:
        \nДалее нужно проверить на сколько правильно нейронная сеть распознала букву.
        \n9. Корректировка:
        \nУправляя яркостью, размытостью изображения(фильтр Гаусса) и контрастностью (порог отсечки) нужно добиться распознавания изображения нейронной сетью. 
        \n10. Приложение Streamlit:
        \nОтображение результатов работы нейронной сети.
        ''')

st.header('Задача',anchor='task')
st.write('Одним из основных источников доходов любого государства являются налоги. Расчет налоговых отчислений является сложной оптимизационной задачей при которой '
         'нужно соблюдать два основных момента. Первый - не разорить предприятие облагаемое налогом. Второй - эффективно наполнить бюджет.')
st.write('Попробуем смоделировать функционирование некоторого гипотетического "государства" , в котором существует несколько ботов(фирм), '
         'а также планировщик налоговых отчислений. Предположим что данное государство существует на квадратном поле размером 25х25 клеток.')

st.image(image_world, caption='Здесь показана среда взаимодействия ботов. Отчетливо видны границы, условно разделяющие все поле на четыре квадрата.'
                              'Границы не сплошные. У ботов есть возможность заходить в соседние квадраты.')

st.write('Мы познакомимся с четырьмя вариантами расчета налоговых отчислений:')
st.write('1) Свободный рынок (Free market).')
st.write('2) Налоговая шкала федеральной системы США. [US Federal](https://www.nerdwallet.com/article/taxes/federal-income-tax-brackets)')
st.write('3) Формула Эммануэля Саеза [Emmanual Saez](https://eml.berkeley.edu/~saez/Saez_photopage_8_1.html).')
st.write('4) AI-налоговик (AI-taxer).')


st.write('Эммануэль Саез - французский и американский экономист, специалист по налоговой политике и неравенству. '
         'Доктор философии, профессор Калифорнийского университета в Беркли и директор его центра Center for Equitable Growth.')
st.sidebar.subheader('Эффективность ботов')
ef1 = st.slider('Агент 1',1,10,5,step=1)
ef2 = st.slider('Агент 2',1,10,3,step=1)
ef3 = st.slider('Агент 3',1,10,2,step=1)
ef4 = st.slider('Агент 4',1,10,1,step=1)

with st.expander('Автоматический расчет налоговых отчислений'):
    st.write('В данной программе представлено несколько примеров расчета налоговых отчислений для'
             'некоторого количества фирм(агентов). Рассматрено четыре метода расчета налогов.')
but_start = st.button('Расчет')

formula1 = st.radio('Каким образом расчитывается налог?', ('Свободный рынок','Налог согласно US Federal','Формула Эммануэля Саеза','AI tax планировщик'))

number1 = st.number_input('Количество итераций',1,20,3,step=1)

my_bar = st.progress(0)

bot1 = [ef1,0]
bot2 = [ef2,0]
bot3 = [ef3,0]
bot4 = [ef4,0]

if but_start:
        st.header('Налог расчитывается как')
        st.subheader(formula1)
        iternum = 0
        st.write('итерация номер:', iternum)
        if formula1 == 'Свободный рынок':
                placeholder = st.empty()
                for percent_complete in range(number1):
                        #time.sleep(0.1)
                        iternum +=1
                        my_bar.progress(percent_complete + 1)
                        bot1[1] = bot1[1] + bot1[0]
                        bot2[1] = bot2[1] + bot2[0]
                        bot3[1] = bot3[1] + bot3[0]
                        bot4[1] = bot4[1] + bot4[0]
                        with placeholder.container():
                                graph_plot.graph_pie(bot1[1], bot2[1], bot3[1], bot4[1])
                                st.write(pd.DataFrame({'Агент №': [1, 2, 3, 4],'Выручка': [bot1[1], bot2[1], bot3[1], bot4[1]], }))


        elif formula1 == 'AI tax планировщик':
                for percent_complete in range(number1):
                        #time.sleep(0.1)
                        st.write('итерация номер:',percent_complete)
                        my_bar.progress(percent_complete + 1)
                        bot1[1] = bot1[1] + bot1[0]
                        bot2[1] = bot2[1] + bot2[0]
                        bot3[1] = bot3[1] + bot3[0]
                        bot4[1] = bot4[1] + bot4[0]

        #graph_plot.graph_pie(bot1[1],bot2[1],bot3[1],bot4[1])




