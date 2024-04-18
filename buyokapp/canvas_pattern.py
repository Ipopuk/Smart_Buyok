import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import buyokapp.config as config


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        super().__init__(fig)
        self.setParent(parent)
        """
        Matplotlib script
        """
        # plt.style.use('_mpl-gallery')

        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        connect = engine.connect()
        all_rows = connect.execute(text('SELECT * FROM metrics')).all()
        depth_metrics = list(map(lambda x: x[3], all_rows))
        delta = max(depth_metrics) - min(depth_metrics)
        border_1 = min(depth_metrics) + 0.2 / 3
        border_2 = min(depth_metrics) + delta / 3 * 2
        print(border_1, border_2)
        first_part = [[], []]
        second_part = [[], []]
        third_part = [[], []]
        for i, row in enumerate(all_rows):
            ll_list = list(map(float, row[2].split(",")))
            latt = ll_list[0]
            long = ll_list[1]
            depth = row[3]
            print(depth, border_2, border_1)
            if depth >= border_2:
                first_part[0].append(latt)
                first_part[1].append(long)
            elif border_2 > depth >= border_1:
                second_part[0].append(latt)
                second_part[1].append(long)
            else:
                third_part[0].append(latt)
                third_part[1].append(long)
        print(first_part, second_part, third_part)

        x_1 = first_part[0]
        y_1 = first_part[1]
        self.ax.scatter(x_1, y_1, c='#003A8E')

        x_2 = second_part[0]
        y_2 = second_part[1]
        self.ax.scatter(x_2, y_2, c='#1F6FE3')

        x_3 = third_part[0]
        y_3 = third_part[1]
        self.ax.scatter(x_3, y_3, c='#C0DAFF')
        self.ax.set(xlabel='Долгота', ylabel='Широта')

