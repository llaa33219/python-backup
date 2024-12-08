import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from matplotlib import font_manager, rc
import os
import matplotlib as mpl

# Function to set Korean font
def set_korean_font():
    # Windows 기본 폰트 경로
    windows_font = 'C:\\Windows\\Fonts\\malgun.ttf'
    nanum_font = 'C:\\Windows\\Fonts\\NanumGothic.ttf'  # 필요시 설치
    
    if os.path.exists(windows_font):
        rc('font', family='Malgun Gothic')
    elif os.path.exists(nanum_font):
        rc('font', family='NanumGothic')
    else:
        print("한국어 폰트를 찾지 못했습니다. 기본 폰트를 사용합니다.")
        # 기본 폰트 설정 (추가 설정 가능)
        rc('font', family='sans-serif')

# Set Korean font
set_korean_font()

# Fix for minus sign glyph
mpl.rcParams['axes.unicode_minus'] = False  # 하이픈 사용

# Define element categories and their colors
category_colors = {
    'Alkali Metal': '#FF6666',
    'Alkaline Earth Metal': '#FFDEAD',
    'Transition Metal': '#FFD700',
    'Post-Transition Metal': '#98FB98',
    'Metalloid': '#87CEFA',
    'Nonmetal': '#D3D3D3',
    'Halogen': '#FFB6C1',
    'Noble Gas': '#B0E0E6',
    'Lanthanide': '#FFA07A',
    'Actinide': '#20B2AA',
    'Unknown': '#FFFFFF'  # 기본 색상
}

# Define Korean names for categories
category_korean = {
    'Alkali Metal': '알칼리 금속',
    'Alkaline Earth Metal': '알칼리 토금속',
    'Transition Metal': '전이 금속',
    'Post-Transition Metal': '준전이 금속',
    'Metalloid': '준금속',
    'Nonmetal': '비금속',
    'Halogen': '할로겐',
    'Noble Gas': '비활성 기체',
    'Lanthanide': '란타넘족',
    'Actinide': '악티늄족',
    'Unknown': '알 수 없음'
}

# Load the complete periodic table data with Korean names and categories
data = [
    # Atomic Number, Symbol, Korean Name, Group, Period, Category
    (1, 'H', '수소', 1, 1, 'Nonmetal'),
    (2, 'He', '헬륨', 18, 1, 'Noble Gas'),
    (3, 'Li', '리튬', 1, 2, 'Alkali Metal'),
    (4, 'Be', '베릴륨', 2, 2, 'Alkaline Earth Metal'),
    (5, 'B', '붕소', 13, 2, 'Metalloid'),
    (6, 'C', '탄소', 14, 2, 'Nonmetal'),
    (7, 'N', '질소', 15, 2, 'Nonmetal'),
    (8, 'O', '산소', 16, 2, 'Nonmetal'),
    (9, 'F', '플루오린', 17, 2, 'Halogen'),
    (10, 'Ne', '네온', 18, 2, 'Noble Gas'),
    (11, 'Na', '나트륨', 1, 3, 'Alkali Metal'),
    (12, 'Mg', '마그네슘', 2, 3, 'Alkaline Earth Metal'),
    (13, 'Al', '알루미늄', 13, 3, 'Post-Transition Metal'),
    (14, 'Si', '규소', 14, 3, 'Metalloid'),
    (15, 'P', '인', 15, 3, 'Nonmetal'),
    (16, 'S', '황', 16, 3, 'Nonmetal'),
    (17, 'Cl', '염소', 17, 3, 'Halogen'),
    (18, 'Ar', '아르곤', 18, 3, 'Noble Gas'),
    (19, 'K', '칼륨', 1, 4, 'Alkali Metal'),
    (20, 'Ca', '칼슘', 2, 4, 'Alkaline Earth Metal'),
    (21, 'Sc', '스칸듐', 3, 4, 'Transition Metal'),
    (22, 'Ti', '티타늄', 4, 4, 'Transition Metal'),
    (23, 'V', '바나듐', 5, 4, 'Transition Metal'),
    (24, 'Cr', '크로뮴', 6, 4, 'Transition Metal'),
    (25, 'Mn', '망가니즈', 7, 4, 'Transition Metal'),
    (26, 'Fe', '철', 8, 4, 'Transition Metal'),
    (27, 'Co', '코발트', 9, 4, 'Transition Metal'),
    (28, 'Ni', '니켈', 10, 4, 'Transition Metal'),
    (29, 'Cu', '구리', 11, 4, 'Transition Metal'),
    (30, 'Zn', '아연', 12, 4, 'Transition Metal'),
    (31, 'Ga', '갈륨', 13, 4, 'Post-Transition Metal'),
    (32, 'Ge', '저마늄', 14, 4, 'Metalloid'),
    (33, 'As', '비소', 15, 4, 'Metalloid'),
    (34, 'Se', '셀레늄', 16, 4, 'Nonmetal'),
    (35, 'Br', '브로민', 17, 4, 'Halogen'),
    (36, 'Kr', '크립톤', 18, 4, 'Noble Gas'),
    (37, 'Rb', '루비듐', 1, 5, 'Alkali Metal'),
    (38, 'Sr', '스트론튬', 2, 5, 'Alkaline Earth Metal'),
    (39, 'Y', '이트륨', 3, 5, 'Transition Metal'),
    (40, 'Zr', '지르코늄', 4, 5, 'Transition Metal'),
    (41, 'Nb', '나이오븀', 5, 5, 'Transition Metal'),
    (42, 'Mo', '몰리브데넘', 6, 5, 'Transition Metal'),
    (43, 'Tc', '테크네튬', 7, 5, 'Transition Metal'),
    (44, 'Ru', '루테늄', 8, 5, 'Transition Metal'),
    (45, 'Rh', '로듐', 9, 5, 'Transition Metal'),
    (46, 'Pd', '팔라듐', 10, 5, 'Transition Metal'),
    (47, 'Ag', '은', 11, 5, 'Post-Transition Metal'),
    (48, 'Cd', '카드뮴', 12, 5, 'Transition Metal'),
    (49, 'In', '인듐', 13, 5, 'Post-Transition Metal'),
    (50, 'Sn', '주석', 14, 5, 'Post-Transition Metal'),
    (51, 'Sb', '안티모니', 15, 5, 'Metalloid'),
    (52, 'Te', '텔루륨', 16, 5, 'Metalloid'),
    (53, 'I', '아이오딘', 17, 5, 'Halogen'),
    (54, 'Xe', '크세논', 18, 5, 'Noble Gas'),
    (55, 'Cs', '세슘', 1, 6, 'Alkali Metal'),
    (56, 'Ba', '바륨', 2, 6, 'Alkaline Earth Metal'),
    # Lanthanides
    (57, 'La', '란타넘', 0, 9, 'Lanthanide'),
    (58, 'Ce', '세륨', 0, 9, 'Lanthanide'),
    (59, 'Pr', '프라세오디뮴', 0, 9, 'Lanthanide'),
    (60, 'Nd', '네오디뮴', 0, 9, 'Lanthanide'),
    (61, 'Pm', '프로메튬', 0, 9, 'Lanthanide'),
    (62, 'Sm', '사마륨', 0, 9, 'Lanthanide'),
    (63, 'Eu', '유로퓸', 0, 9, 'Lanthanide'),
    (64, 'Gd', '가돌리늄', 0, 9, 'Lanthanide'),
    (65, 'Tb', '터븀', 0, 9, 'Lanthanide'),
    (66, 'Dy', '디스프로슘', 0, 9, 'Lanthanide'),
    (67, 'Ho', '홀뮴', 0, 9, 'Lanthanide'),
    (68, 'Er', '어븀', 0, 9, 'Lanthanide'),
    (69, 'Tm', '툴륨', 0, 9, 'Lanthanide'),
    (70, 'Yb', '이터븀', 0, 9, 'Lanthanide'),
    (71, 'Lu', '루테튬', 0, 9, 'Lanthanide'),
    (72, 'Hf', '하프늄', 4, 6, 'Transition Metal'),
    (73, 'Ta', '탄탈럼', 5, 6, 'Transition Metal'),
    (74, 'W', '텅스텐', 6, 6, 'Transition Metal'),
    (75, 'Re', '레늄', 7, 6, 'Transition Metal'),
    (76, 'Os', '오스뮴', 8, 6, 'Transition Metal'),
    (77, 'Ir', '이리듐', 9, 6, 'Transition Metal'),
    (78, 'Pt', '백금', 10, 6, 'Transition Metal'),
    (79, 'Au', '금', 11, 6, 'Transition Metal'),
    (80, 'Hg', '수은', 12, 6, 'Transition Metal'),
    (81, 'Tl', '탈륨', 13, 6, 'Post-Transition Metal'),
    (82, 'Pb', '납', 14, 6, 'Post-Transition Metal'),
    (83, 'Bi', '비스무트', 15, 6, 'Post-Transition Metal'),
    (84, 'Po', '폴로늄', 16, 6, 'Metalloid'),
    (85, 'At', '아스타틴', 17, 6, 'Halogen'),
    (86, 'Rn', '라돈', 18, 6, 'Noble Gas'),
    (87, 'Fr', '프랑슘', 1, 7, 'Alkali Metal'),
    (88, 'Ra', '라듐', 2, 7, 'Alkaline Earth Metal'),
    # Actinides
    (89, 'Ac', '악티늄', 0, 10, 'Actinide'),
    (90, 'Th', '토륨', 0, 10, 'Actinide'),
    (91, 'Pa', '프로트악티늄', 0, 10, 'Actinide'),
    (92, 'U', '우라늄', 0, 10, 'Actinide'),
    (93, 'Np', '넵투늄', 0, 10, 'Actinide'),
    (94, 'Pu', '플루토늄', 0, 10, 'Actinide'),
    (95, 'Am', '아메리슘', 0, 10, 'Actinide'),
    (96, 'Cm', '퀴륨', 0, 10, 'Actinide'),
    (97, 'Bk', '버클륨', 0, 10, 'Actinide'),
    (98, 'Cf', '캘리포늄', 0, 10, 'Actinide'),
    (99, 'Es', '아인슈타이늄', 0, 10, 'Actinide'),
    (100, 'Fm', '페르뮴', 0, 10, 'Actinide'),
    (101, 'Md', '멘델레븀', 0, 10, 'Actinide'),
    (102, 'No', '노벨륨', 0, 10, 'Actinide'),
    (103, 'Lr', '로렌슘', 0, 10, 'Actinide'),
    (104, 'Rf', '러더포듐', 4, 7, 'Transition Metal'),
    (105, 'Db', '더브늄', 5, 7, 'Transition Metal'),
    (106, 'Sg', '시보귬', 6, 7, 'Transition Metal'),
    (107, 'Bh', '보륨', 7, 7, 'Transition Metal'),
    (108, 'Hs', '하슘', 8, 7, 'Transition Metal'),
    (109, 'Mt', '마이트너륨', 9, 7, 'Transition Metal'),
    (110, 'Ds', '다름슈타튬', 10, 7, 'Transition Metal'),
    (111, 'Rg', '뢴트게늄', 11, 7, 'Transition Metal'),
    (112, 'Cn', '코페르니슘', 12, 7, 'Transition Metal'),
    (113, 'Nh', '니호늄', 13, 7, 'Post-Transition Metal'),
    (114, 'Fl', '플레로븀', 14, 7, 'Post-Transition Metal'),
    (115, 'Mc', '모스코븀', 15, 7, 'Post-Transition Metal'),
    (116, 'Lv', '리버모륨', 16, 7, 'Post-Transition Metal'),
    (117, 'Ts', '테네신', 17, 7, 'Halogen'),
    (118, 'Og', '오가네손', 18, 7, 'Noble Gas')
]

df = pd.DataFrame(data, columns=['AtomicNumber', 'Symbol', 'KoreanName', 'Group', 'Period', 'Category'])

# Separate lanthanides and actinides
lanthanides = df[df['Category'] == 'Lanthanide']
actinides = df[df['Category'] == 'Actinide']

# Main table excludes lanthanides and actinides
main_table = df[(df['Period'] <= 7) & (df['Period'] >=1) & (df['Group'] !=0) & (~df['Category'].isin(['Lanthanide', 'Actinide']))]

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(19.2, 12))  # 높이를 늘려 별도 행을 수용
ax.set_xlim(0, 18)
ax.set_ylim(-3, 10)
ax.axis('off')

# Draw main table elements
for _, row in main_table.iterrows():
    group = row['Group']
    period = row['Period']
    atomic_number = row['AtomicNumber']
    symbol = row['Symbol']
    korean_name = row['KoreanName']
    category = row['Category']
    
    color = category_colors.get(category, category_colors['Unknown'])
    
    # Adjust y position (main table from y=0 to y=7)
    y = 7 - period
    
    # Draw rectangle
    rect = patches.Rectangle((group - 1, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    
    # Add texts
    plt.text(group - 0.95, y + 0.8, atomic_number, horizontalalignment='left', verticalalignment='top', fontsize=8)
    plt.text(group - 0.5, y + 0.5, symbol, horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')
    plt.text(group - 0.5, y + 0.2, korean_name, horizontalalignment='center', verticalalignment='center', fontsize=8)

# Add merged cells for Lanthanides and Actinides in main table

# Define the positions and sizes
# Period 6: y = 7 - 6 = 1
# Period 7: y = 7 - 7 = 0

# Lanthanides: Period 6, Groups 3-12 (x=2 to x=11)
lan_main_x = 2 - 1  # Group 3 starts at x=2, so x=1
lan_main_y = 7 - 6  # y=1
lan_main_width = 10  # Groups 3-12
lan_main_height = 1

# Actinides: Period 7, Groups 3-12 (x=2 to x=11)
act_main_x = 2 - 1  # x=1
act_main_y = 7 - 7  # y=0
act_main_width = 10
act_main_height = 1

# Draw rectangles for Lanthanides and Actinides in main table
# Use a distinct color or hatch to indicate these merged cells
merged_color = 'lightgrey'
hatch_pattern = '////'

rect_lan_main = patches.Rectangle((lan_main_x, lan_main_y), lan_main_width, lan_main_height,
                                  linewidth=1, edgecolor='black', facecolor=merged_color, hatch=hatch_pattern)
ax.add_patch(rect_lan_main)

rect_act_main = patches.Rectangle((act_main_x, act_main_y), act_main_width, act_main_height,
                                  linewidth=1, edgecolor='black', facecolor=merged_color, hatch=hatch_pattern)
ax.add_patch(rect_act_main)

# Add texts inside the merged cells
plt.text(lan_main_x + lan_main_width / 2, lan_main_y + lan_main_height / 2,
         '57~71\nLanthanide\n란타넘족',
         horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')

plt.text(act_main_x + act_main_width / 2, act_main_y + act_main_height / 2,
         '89~103\nActinide\n악티늄족',
         horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')

# Draw lanthanides in separate row
lan_y = -1  # y position for lanthanides
for idx, row in lanthanides.iterrows():
    atomic_number = row['AtomicNumber']
    symbol = row['Symbol']
    korean_name = row['KoreanName']
    category = row['Category']
    
    color = category_colors.get(category, category_colors['Unknown'])
    
    x = row['AtomicNumber'] - 57  # Position lanthanides in separate row starting at x=0
    
    # Draw rectangle
    rect = patches.Rectangle((x, lan_y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    
    # Add texts
    plt.text(x + 0.05, lan_y + 0.8, atomic_number, horizontalalignment='left', verticalalignment='top', fontsize=8)
    plt.text(x + 0.5, lan_y + 0.5, symbol, horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')
    plt.text(x + 0.5, lan_y + 0.2, korean_name, horizontalalignment='center', verticalalignment='center', fontsize=8)

# Draw actinides in separate row
act_y = -2  # y position for actinides
for idx, row in actinides.iterrows():
    atomic_number = row['AtomicNumber']
    symbol = row['Symbol']
    korean_name = row['KoreanName']
    category = row['Category']
    
    color = category_colors.get(category, category_colors['Unknown'])
    
    x = row['AtomicNumber'] - 89  # Position actinides in separate row starting at x=0
    
    # Draw rectangle
    rect = patches.Rectangle((x, act_y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    
    # Add texts
    plt.text(x + 0.05, act_y + 0.8, atomic_number, horizontalalignment='left', verticalalignment='top', fontsize=8)
    plt.text(x + 0.5, act_y + 0.5, symbol, horizontalalignment='center', verticalalignment='center', fontsize=10, fontweight='bold')
    plt.text(x + 0.5, act_y + 0.2, korean_name, horizontalalignment='center', verticalalignment='center', fontsize=8)

# Add labels for lanthanides and actinides (separate rows)
plt.text(-1, lan_y + 0.5, '란타넘족', horizontalalignment='right', verticalalignment='center', fontsize=12, fontweight='bold')
plt.text(-1, act_y + 0.5, '악티늄족', horizontalalignment='right', verticalalignment='center', fontsize=12, fontweight='bold')

# Add title
plt.title('주기율표 (한국어 명칭 포함)', fontsize=20)

# Create a legend
from matplotlib.patches import Patch

# Create legend elements with Korean labels
legend_elements = [Patch(facecolor=color, edgecolor='black', label=category_korean[category]) 
                   for category, color in category_colors.items() if category not in ['Unknown']]

plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1), title='카테고리')

# Adjust layout to make space for labels
plt.tight_layout()

# Save the plot as a file
plt.savefig('9periodic_table_full_korean_colored.png', bbox_inches='tight')

# Show the plot
plt.show()
