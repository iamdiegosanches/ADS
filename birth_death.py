import pandas as pd
import numpy as np

def calculate_finite_queue(capacity: int, arrival_fn, service_fn):
    k_values = np.arange(capacity + 1)
    df = pd.DataFrame({'k': k_values})

    df['lambda'] = df['k'].apply(arrival_fn)
    df['mu'] = df['k'].apply(service_fn)

    prev_lambda = df['lambda'].shift(1) 
    
    df['ratio'] = prev_lambda / df['mu']
    df.loc[0, 'ratio'] = 1.0

    df['coef'] = df['ratio'].cumprod()

    p0 = 1.0 / df['coef'].sum()
    df['prob'] = df['coef'] * p0

    avg_number_L = (df['k'] * df['prob']).sum()
    throughput_X = (df['mu'] * df['prob']).sum()

    avg_time_W = avg_number_L / throughput_X if throughput_X > 0 else 0.0

    return {
        "metrics": {
            "L (Avg System Size)": avg_number_L,
            "X (Throughput)": throughput_X,
            "W (Avg Response Time)": avg_time_W,
            "P_blocking": df.iloc[-1]['prob'] 
        },
        "state_table": df[['k', 'lambda', 'mu', 'prob']]
    }
