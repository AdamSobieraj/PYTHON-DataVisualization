import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Przygotowanie danych
KGHM_akcje = pd.read_csv('data/kgh_d.csv')
cena_miedzi = pd.read_csv('data/ca_c_f_d.csv')

# Usuwanie wartości NULL i poprawa formatu kolumny 'Data'
KGHM_akcje = KGHM_akcje.dropna(subset=['Data'])
cena_miedzi = cena_miedzi.dropna(subset=['Data'])

# Konwersja kolumny 'Data' do formatu datetime
KGHM_akcje['Data'] = pd.to_datetime(KGHM_akcje['Data'])
cena_miedzi['Data'] = pd.to_datetime(cena_miedzi['Data'])

# Połączenie danych z obu plików CSV
combined_data = pd.merge(KGHM_akcje[['Data', 'Zamkniecie']], cena_miedzi[['Data', 'Zamkniecie']], on='Data', how='outer')

# Usuwanie wartości NULL z połączonego DataFrame
combined_data = combined_data.dropna()

# Tworzenie subplots z odpowiednim typem dla tabeli
fig = make_subplots(
    rows=3,
    cols=1,
    specs=[
        [{"type": "xy"}],
        [{"type": "xy"}],
        [{"type": "table"}]
    ],
    subplot_titles=("Ceny zamknięcia KGHM", "Ceny miedzi", "Tabela zestawienia")
)

# Tworzenie pierwszego wykresu - ceny zamknięcia KGHM
trace1 = go.Scatter(
    x=combined_data['Data'],
    y=combined_data['Zamkniecie_y'],
    mode='lines',
    name='KGHM'
)
fig.add_trace(trace1, row=1, col=1)

# Tworzenie drugiego wykresu - ceny miedzi
trace2 = go.Scatter(
    x=combined_data['Data'],
    y=combined_data['Zamkniecie_x'],
    mode='lines',
    name='Miedź'
)
fig.add_trace(trace2, row=2, col=1)

# Dodanie tabeli zestawienia
table_data = combined_data[['Data', 'Zamkniecie_y','Zamkniecie_x']]

# Konwersja kolumny 'Data' do formatu datetime w DataFrame table_data
table_data['Data'] = pd.to_datetime(table_data['Data'])

# Formatowanie kolumny 'Data' jako postaciowego dnia miesiąca roku
table_data['Data'] = table_data['Data'].dt.strftime('%d.%m.%Y')


fig.add_trace(go.Table(
    header=dict(values=['Data', 'KGHM', 'Miedź'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[table_data['Data'], table_data['Zamkniecie_y'], table_data['Zamkniecie_x']], fill_color='lightgrey', align='left')
), row=3, col=1)

# Konfiguracja layoutu
fig.update_layout(height=1000, showlegend=True)

# Wyświetlanie wykresu
fig.show()
