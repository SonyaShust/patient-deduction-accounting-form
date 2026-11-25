import matplotlib
matplotlib.use("TkAgg")           # backend для встраивания в Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def build_stats_figure(patients) -> Figure:
    """Возвращает Figure с 4 графиками в сетке 2x2."""
    fig = Figure(figsize=(10, 7), dpi=90)
    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    ages = [p.age for p in patients]
    genders = [p.gender for p in patients]
    bmis = [p.bmi for p in patients]

    ax1 = fig.add_subplot(221)
    m_count = genders.count("М")
    w_count = genders.count("Ж")
    n_count = genders.count("Не определен")
    if m_count + w_count:
        ax1.pie([m_count, w_count, n_count], labels=["М", "Ж", "не определен"],
                autopct="%1.0f%%", colors=["#4C72B0", "#DD8452", "#B04CAB"])
    ax1.set_title("Пол")

    # гистограмма
    ax2 = fig.add_subplot(222)
    ax2.hist(ages, bins=range(0, 121, 10), edgecolor="black",
             color="#55A868")
    ax2.set_title("Возраст")
    ax2.set_xlabel("Лет")

    # ИМТ
    ax3 = fig.add_subplot(223)
    bmi_m = [p.bmi for p in patients if p.gender == "М"]
    bmi_w = [p.bmi for p in patients if p.gender == "Ж"]
    bmi_n = [p.bmi for p in patients if p.gender == "не определен"]
    bins = [15, 18.5, 20, 22.5, 25, 27.5, 30, 35, 40]
    if bmi_m:
        ax3.hist(bmi_m, bins=bins, alpha=0.6, label="М", color="#4C72B0")
    if bmi_w:
        ax3.hist(bmi_w, bins=bins, alpha=0.6, label="Ж", color="#DD8452")
    if bmi_n:
            ax3.hist(bmi_m, bins=bins, alpha=0.6, label="М", color="#B04CAB")
    ax3.set_title("ИМТ по полу")
    ax3.set_xlabel("ИМТ")
    ax3.legend()

    # ИМТ от возраста
    ax4 = fig.add_subplot(224)
    for gender, color, label in [("М", "#4C72B0", "М"), ("Ж", "#DD8452", "Ж"), ("не определен", "#B04CAB", "не определен")]:
        xs = [p.age for p in patients if p.gender == gender]
        ys = [p.bmi for p in patients if p.gender == gender]
        ax4.scatter(xs, ys, color=color, label=label, alpha=0.75)
    ax4.set_title("ИМТ от возраста")
    ax4.set_xlabel("Возраст")
    ax4.set_ylabel("ИМТ")
    ax4.legend()

    return fig