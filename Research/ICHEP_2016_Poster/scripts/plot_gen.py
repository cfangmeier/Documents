#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np




def plot_ph():
    np.random.seed(0)
    fig = plt.figure()
    ax = fig.gca()
    N = 100
    x_lim = (0, 100)
    mu = 40
    sig = 7
    xs = np.linspace(*x_lim, num=N)
    bg = np.random.poisson(lam=100, size=N)/30
    sig = 10*np.exp(-(xs-mu)**2/sig**2)
    dat = sig+bg
    ax.plot(xs, dat)
    pt_x, pt_y = xs[40], dat[40]
    ax.annotate("", xy=(pt_x-15, pt_y), xytext=(pt_x-15, 0),
                arrowprops=dict(arrowstyle="|-|", color='k'))

    samples_x = xs[1::20]
    samples_y = dat[1::20]
    ax.plot(samples_x, samples_y, 'ro')
    for s_x, s_y in zip(samples_x[0:], samples_y[0:]):
        ax.annotate("Sample Points",
                    xy=(s_x, s_y),
                    xytext=(60, 10),
                    arrowprops=dict(arrowstyle="-|>", color='r'))
    ax.text(pt_x-19.8, 12.5, "Pulse Height", rotation='vertical')
    ax.plot([pt_x, pt_x-15], [pt_y, pt_y], 'k--')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', top='off')
    ax.tick_params(axis='x', labelbottom='off')
    ax.tick_params(axis='y', right='off')
    ax.tick_params(axis='y', labelleft='off')
    ax.set_xlim(x_lim)
    ax.set_ylim((0, max(dat)*1.2))
    ax.set_xlabel('time')
    ax.set_ylabel('current')
    fig.savefig("../figures/signal_pulse.svg")
    # plt.show()


def step_curve_data(N, mu=None, sigma=None, seed=0):
    np.random.seed(seed)
    xs = np.array(range(N))
    bg = np.random.poisson(lam=100, size=N)/30 - 1.5
    if mu is not None and sigma is not None:
        sig = 10*np.exp(-(xs-mu)**2/sigma**2)
        return xs, sig+bg
    else:
        return xs, bg


def plot_step_curve():
    fig = plt.figure()
    ax = fig.gca()
    x_lim = (0, 20)
    N = 20
    mu = 7
    sigma = 1
    xs, dat = step_curve_data(N, mu, sigma)
    dat_xs = []
    dat_ys = []
    for x, d in zip(xs, dat):
        dat_xs.append(x+0.1)
        dat_ys.append(d)
        dat_xs.append(x+0.9)
        dat_ys.append(d)

    ax.plot(dat_xs, dat_ys)
    ax.annotate("", xy=(6.1, 11.5), xytext=(8.9, 11.5),
                arrowprops=dict(arrowstyle="|-|", color='k'))
    ax.text(9.0, 11.0, "Charge shared among \n3 strips")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', top='off')
    ax.tick_params(axis='y', right='off')
    ax.tick_params(axis='y', labelleft='off')
    ax.set_xlim(x_lim)
    ax.set_ylim((0, max(dat)*1.2))
    ax.set_xlabel('Strip #')
    ax.set_ylabel('voltage')
    fig.tight_layout()
    fig.savefig("../figures/step_curve.svg")
    # plt.show()


def single_dig_waveform(ax, i_form, v_scale=0.75):
    N = 10
    mu = 7
    sigma = 1
    if not i_form % 2:
        xs, dat = step_curve_data(N*2, mu, sigma, seed=i_form)
    else:
        xs, dat = step_curve_data(N*2, seed=i_form)
    xs = np.array(range(N))[:7]
    plot_xs = []
    plot_ysp = []
    plot_ysn = []
    for i, x in enumerate(xs):
        plot_xs.append(x-.05)
        plot_ysp.append(.25+i_form*v_scale)
        plot_ysn.append(-.25+i_form*v_scale)
        plot_xs.append(x+.05)
        plot_ysp.append(-.25+i_form*v_scale)
        plot_ysn.append(.25+i_form*v_scale)
        plot_xs.append(x+.45)
        plot_ysp.append(-.25+i_form*v_scale)
        plot_ysn.append(.25+i_form*v_scale)
        plot_xs.append(x+.55)
        plot_ysp.append(.25+i_form*v_scale)
        plot_ysn.append(-.25+i_form*v_scale)
        ph = dat[i*2]*10
        ax.text(x+.25, i_form*v_scale, str(int(ph)),
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=16)
        ph = dat[i*2+1]*10
        ax.text(x+.75, i_form*v_scale, str(int(ph)),
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=16)
    plot_xs = np.array(plot_xs)
    plot_ysp = np.array(plot_ysp)
    plot_ysn = np.array(plot_ysn)
    ax.plot(plot_xs, plot_ysp, 'k')
    ax.plot(plot_xs, plot_ysn, 'k')
    if i_form == 0:
        for i, d in enumerate(dat[:13]):
            ax.plot([i/2, i/2, i/2+.55], [2.5, -0.5, -1.05], '--g')
            ax.text(i/2+.08, -.5, "strip {}".format(i+1),
                    rotation=-45,
                    fontsize=18)


def plot_dig_waveform():
    fig = plt.figure()
    ax = fig.gca()
    for i in range(4):
        single_dig_waveform(ax, i)
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', bottom='off', top='off')
    ax.tick_params(axis='x', labelbottom='off')
    ax.tick_params(axis='y', left='off', right='off')
    ax.tick_params(axis='y', labelleft='off')
    ax.set_ylim((-1.1, 3.5))
    fig.savefig("../figures/dig_waveform.svg", dpi=300)
    # plt.show()


def main():
    with plt.xkcd():
        mpl.rcParams.update({'font.size': 26})
        pass
        plot_ph()
        plot_step_curve()
        plot_dig_waveform()

if __name__ == '__main__':
    main()
