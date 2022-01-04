from matplotlib import pyplot as plt
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('times.csv')
    plain = df.A
    ab = df.B
    n_blanks = range(1, 10)
    plt.plot(n_blanks, plain, label='Mini-Max search', linewidth=0.5, marker='x')
    plt.plot(n_blanks, ab, label=r'$\alpha$-$\beta$ pruning', linewidth=0.5, marker='x')
    plt.yscale('log')
    plt.grid(which='major')
    plt.ylabel('elapsed time [sec]')
    plt.xlabel('number of blanks')
    plt.legend()
    plt.show()
