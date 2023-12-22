import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import plotly.express as px
import jieba
import re
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

def get_text_from_url(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确处理字符编码
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.body.get_text()

def clean_text_for_count(text):
    text = re.sub('<.*?>', '', text)  # 去除HTML标签
    text = re.sub('[^\w\s]', '', text)  # 去除标点符号
    text = re.sub('\s', '', text)  # 去除空格
    return text
def clean_text_for_preview(text):
    text = re.sub('<.*?>', '', text)  # 去除HTML标签
    return text

def get_top_words(text, num_words):
    text = clean_text_for_count(text)
    if any("\u4e00" <= ch <= "\u9fff" for ch in text):  # 检查是否有中文字符
        words = jieba.lcut(text)  # 使用jieba进行中文分词
    else:
        words = word_tokenize(text)  # 使用nltk进行英文分词
    counter = Counter(words)
    return counter.most_common(num_words) if words else []

def draw_wordcloud(text, color):
    if text:  # 检查text是否为空
        wordcloud = WordCloud(font_path='./SimHei.ttf', background_color=color).generate(text)  # 使用用户选择的颜色
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt
    else:
        return None

def draw_pie_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.pie(df, values='counts', names='words', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_bar_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.bar(df, x='words', y='counts', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_line_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.line(df, x='words', y='counts', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_scatter_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.scatter(df, x='words', y='counts', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_area_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.area(df, x='words', y='counts', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_radar_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.line_polar(df, r='counts', theta='words', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

def draw_box_chart(word_counts):
    if word_counts:  # 检查word_counts列表是否为空
        words, counts = zip(*word_counts)
        df = pd.DataFrame({'words': words, 'counts': counts})  # 创建数据框
        fig = px.box(df, y='counts', title='词频统计', hover_data=['counts'], labels={'counts':'出现次数'})
        return fig
    else:
        return None

# Streamlit应用程序
def main():
    st.title('网址分析')
    url = st.text_input('请输入网址')
    chart_style = st.sidebar.selectbox('设置统计图样式',
                                       ['饼图', '柱状图', '折线图', '散点图', '面积图', '雷达图', '箱线图'])  # 添加下拉框
    num_words = st.sidebar.slider('设置高频词汇数量', min_value=1, max_value=50, value=20)
    if url:
        text = get_text_from_url(url)
    else:
        text = None
    if text is not None:
        clean_text_preview = clean_text_for_preview(text)
        clean_text_preview = re.sub('\s+', '\n', clean_text_preview)  # 将连续的空格替换为换行
        word_counts = get_top_words(text, num_words)
        words, _ = zip(*word_counts)
        fig_wordcloud = draw_wordcloud(text,'#000000')
        if chart_style == '饼图':
            fig_chart = draw_pie_chart(word_counts)
        elif chart_style == '柱状图':
            fig_chart = draw_bar_chart(word_counts)
        elif chart_style == '折线图':
            fig_chart = draw_line_chart(word_counts)
        elif chart_style == '散点图':
            fig_chart = draw_scatter_chart(word_counts)
        elif chart_style == '面积图':
            fig_chart = draw_area_chart(word_counts)
        elif chart_style == '雷达图':
            fig_chart = draw_radar_chart(word_counts)
        elif chart_style == '箱线图':
            fig_chart = draw_box_chart(word_counts)
        else:
            fig_chart = None
        if fig_chart is not None:  # 检查fig_chart是否为空
            st.plotly_chart(fig_chart)
        if fig_wordcloud is not None:  # 检查fig_wordcloud是否为空
            st.text("词云图")  # 在代码上方显示“词云图”几个字
            st.pyplot(fig_wordcloud)  # 展示词云图

        st.text_area("文本内容", clean_text_preview, height=250)  # 设置预览框的高度以显示更多内容

# 运行Streamlit应用程序
if __name__ == "__main__":
    main()