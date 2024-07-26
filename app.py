import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.title("Kiểm Định Giả Thuyết Về Điểm Thi Ngoại Ngữ THPTQG2024")

# Đọc dữ liệu từ CSV
thptqg_scores = pd.read_csv('diem_thi_thpt_2024.csv', dtype={'sbd': str})
diem_ngoai_ngu = thptqg_scores['ngoai_ngu'].dropna()

# Thiết lập bins cho điểm
bins = np.round(np.arange(0, 10.2, 0.2), 1)

# Tính toán số lượng điểm
count_diem_ngoai_ngu = diem_ngoai_ngu.value_counts().reindex(bins, fill_value=0).sort_index()

# Tạo biểu đồ phân phối điểm
fig, ax = plt.subplots(figsize=(14, 8))
bar_chart = ax.bar(count_diem_ngoai_ngu.index, count_diem_ngoai_ngu.values, width=0.1, edgecolor='k')

for bar in bar_chart:
    y_height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, y_height + 1000, int(y_height), va='bottom', ha='center', rotation=90)

ax.set_title('Phổ điểm môn Anh Văn kì thi THPTQG 2024')
ax.set_xlabel('Điểm thi')
ax.set_ylabel('Số lượng thí sinh')
ax.set_xticks(count_diem_ngoai_ngu.index)
ax.set_xticklabels([f'{x:.1f}' for x in count_diem_ngoai_ngu.index], rotation=90)
ax.set_yticks(np.arange(0, 60000, 10000))

st.markdown("### **I. Phổ Điểm Thi Ngoại Ngữ Cả Nước THPTQG2024**")
st.write("Ta nhận xét thấy rằng phổ điểm thi ngoại ngữ trong kì thi THPTQG2024 có dạng phân phối đa thức (multimodel distribution), điều này khác hoàn toàn so với các phổ điểm môn khác. Từ đó ta đặt giả thiết rằng có lẽ sự chênh lệch như vậy đến từ việc các thí sinh ở các thành phố lớn được tiếp cận tiếng anh nhiều hơn so với các thí sinh ở tỉnh khác. ")
st.pyplot(fig)

# Điểm thi các thành phố lớn
sbd_HCM = thptqg_scores[thptqg_scores['sbd'].astype(str).str.startswith('02')]
HCM_ngoai_ngu = sbd_HCM['ngoai_ngu'].value_counts().reindex(bins, fill_value=0).sort_index()

sbd_HaNoi = thptqg_scores[thptqg_scores['sbd'].astype(str).str.startswith('01')]
HaNoi_ngoai_ngu = sbd_HaNoi['ngoai_ngu'].value_counts().reindex(bins, fill_value=0).sort_index()

sbd_DaNang = thptqg_scores[thptqg_scores['sbd'].astype(str).str.startswith('04')]
DaNang_ngoai_ngu = sbd_DaNang['ngoai_ngu'].value_counts().reindex(bins, fill_value=0).sort_index()

sbd_CanTho = thptqg_scores[thptqg_scores['sbd'].astype(str).str.startswith('55')]
CanTho_ngoai_ngu = sbd_CanTho['ngoai_ngu'].value_counts().reindex(bins, fill_value=0).sort_index()

# Biểu đồ so sánh điểm các thành phố lớn
fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(HCM_ngoai_ngu.index, HCM_ngoai_ngu.values, width=0.2, edgecolor='k', alpha=0.5, label='HCM')
ax.bar(HaNoi_ngoai_ngu.index, HaNoi_ngoai_ngu.values, width=0.2, color='red', edgecolor='k', alpha=0.5, label='HaNoi')
ax.bar(DaNang_ngoai_ngu.index, DaNang_ngoai_ngu.values, width=0.2, color='green', edgecolor='k', alpha=0.5, label='DaNang')
ax.bar(CanTho_ngoai_ngu.index, CanTho_ngoai_ngu.values, width=0.2, color='grey', edgecolor='k', alpha=0.5, label='CanTho')

ax.set_title('Phổ điểm các thành phố lớn')
ax.set_xlabel('Điểm Thi')
ax.set_ylabel('Số lượng thí sinh')
ax.set_xticks(bins)
ax.set_xticklabels([f'{x:.1f}' for x in bins], rotation=90)
ax.legend()
st.markdown("### **II. Phổ Điểm Các Thành Phố Lớn**")
st.write("Từ hình phổ điểm bên dưới, ta thấy rằng phổ điểm của thủ đô Hà Nội có phân phối đa thức (multimodel distribution) rõ rệt nhất so với các thành phố còn lại, điều này có thể giải thích vì Hà Nội còn có các quận và huyện nhỏ lẻ khác ngoại ô và nội ô, vì thế có phân phối phổ điểm như vậy. Nếu ta breakdown nhỏ xuống ở thành phố Hà Nội xuống cấp quận, huyện, thì phổ điểm sẽ về dạng phân phối chuẩn.")
st.pyplot(fig)

# Tính toán điểm trung bình
big_cities_score = pd.concat([sbd_HCM['ngoai_ngu'], sbd_HaNoi['ngoai_ngu'], sbd_DaNang['ngoai_ngu'], sbd_CanTho['ngoai_ngu']]).dropna()
mean_big_cities = big_cities_score.mean()

whole_country_ngoai_ngu = thptqg_scores['ngoai_ngu'].astype(float)
mean_whole_country = whole_country_ngoai_ngu.mean()

# Biểu đồ so sánh điểm trung bình
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar('Big Cities', mean_big_cities, width=0.2, label='Big Cities')
ax.bar('Whole Country', mean_whole_country, width=0.2, label='Whole Country')

ax.set_title('So Sánh Điểm TB Cả Nước và Các Thành Phố Lớn')
ax.legend()
st.markdown("### **IV. Điểm Trung Bình giữa Cả Nước Và Các Thành Phố Lớn**")
st.write(f'**Trung bình điểm các thành phố lớn:** {mean_big_cities:.4f}')
st.write(f'**Trung bình điểm của cả nước:** {mean_whole_country:.4f}')
st.write("Từ giá trị trung bình trên ta càng có thêm căn cứ để kết luận giả thiết đặt ra ban đầu")
st.pyplot(fig)

# Kiểm định giả thuyết thống kê
t_test, p_value = stats.ttest_ind(big_cities_score, diem_ngoai_ngu)
st.write("Để kiểm tra xem có ý nghĩa thống kê hay không, ta kiểm định bằng T-test, sau khi tính toán ta thu được giá trị statistic và p_value như sau:")

st.write(f'**T-Statistic:** {t_test:.4f}')
st.write(f'**p-Value:** {p_value:.4f}')
st.write("Ta nhận thấy rằng p_value < 0.05 (mức ý nghĩa) như vậy ta kết luận rằng:")
if p_value < 0.05:
    st.write("**Có căn cứ để nói rằng các thí sinh ở các thành phố lớn được tiếp cận tiếng anh cao hơn các tỉnh khác**")
else:
    st.write("**Không có cứ để nói rằng các thí sinh ở các thành phố lớn được tiếp cận tiếng anh cao hơn các tỉnh khác**")
