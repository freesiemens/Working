#import mars.data as mars_data
import numpy as np
import time


def mean_loss(X,n_folds):
    loss = 0
    n_samps = X.shape[0]
    per_fold = n_samps // n_folds
    pop_mean = X.mean(0)
    for i in xrange(0, n_samps, per_fold):
        fold_mean = X[i:i+per_fold].mean(0)
        loss += np.linalg.norm(pop_mean - fold_mean)
    return loss


def multitask_stratified_splitter(X,n_folds,hours=24,fname='best_split.txt'):
    start_time = time.time()
    n_samples = X.shape[0]
    best_error = np.inf
    best_perm = np.arange(X.shape[0])

    while time.time() - start_time < hours * 3600:
        permutation = np.random.permutation(n_samples)
        perm_error = mean_loss(X[permutation],n_folds)
        if best_error - perm_error > 1e-7:
            best_error = perm_error
            best_perm = permutation
            print best_error
            np.savetxt(fname,best_perm,fmt='%d',newline=',')

    return best_perm


def evaluate_split(X,n_folds):
    samp_mean = X.mean(0)
    per_fold = len(X) / n_folds
    print
    for i in xrange(n_folds):
        print i, np.linalg.norm(samp_mean - X[i*per_fold:i*per_fold+per_fold].mean(0))


if __name__ == '__main__':
    #century_labels = mars_data.load_clean_century_labels()
    #century_order = multitask_stratified_splitter(century_labels,10,hours=24,fname='best_century.txt')

    ryans_labels = np.genfromtxt('CCAM_database_for_strat_partition_noduplicates.csv', delimiter=',')[1:, 1:]
    ryans_order = multitask_stratified_splitter(ryans_labels,7,hours=24,fname='best_ryans.txt') 
    evaluate_split(ryans_labels,7)
    evaluate_split(ryans_labels[ryans_order],7)
