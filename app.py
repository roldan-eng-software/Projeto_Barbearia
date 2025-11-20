from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'barbershop.db'

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Tabela de barbeiros
        c.execute('''CREATE TABLE barbeiros
                     (id INTEGER PRIMARY KEY,
                      nome TEXT NOT NULL,
                      especialidade TEXT)''')
        
        # Tabela de agendamentos
        c.execute('''CREATE TABLE agendamentos
                     (id INTEGER PRIMARY KEY,
                      cliente TEXT NOT NULL,
                      barbeiro_id INTEGER NOT NULL,
                      data TEXT NOT NULL,
                      horario TEXT NOT NULL,
                      servico TEXT NOT NULL,
                      valor REAL,
                      status TEXT DEFAULT 'agendado',
                      FOREIGN KEY(barbeiro_id) REFERENCES barbeiros(id))''')
        
        # Insere alguns barbeiros de exemplo
        barbeiros = [
            ('João Silva', 'Corte Clássico'),
            ('Carlos Santos', 'Barba e Desenho'),
            ('Pedro Oliveira', 'Corte Moderno')
        ]
        c.executemany('INSERT INTO barbeiros (nome, especialidade) VALUES (?, ?)', barbeiros)
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados criado com sucesso!")

def get_db():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Página de agendamento"""
    return render_template('index.html')

@app.route('/api/barbeiros')
def get_barbeiros():
    """Retorna lista de barbeiros em JSON"""
    conn = get_db()
    c = conn.cursor()
    barbeiros = c.execute('SELECT id, nome, especialidade FROM barbeiros').fetchall()
    conn.close()
    return jsonify([dict(b) for b in barbeiros])

@app.route('/api/horarios-disponiveis', methods=['POST'])
def horarios_disponiveis():
    """Retorna horários disponíveis para um barbeiro em uma data"""
    try:
        dados = request.get_json()
        data = dados.get('data')
        barbeiro_id = dados.get('barbeiro_id')
        
        if not data or not barbeiro_id:
            return jsonify({'erro': 'Data e barbeiro são obrigatórios'}), 400
        
        # Horários de funcionamento (9h às 18h, intervalos de 30min)
        horarios = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                    '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30']
        
        conn = get_db()
        c = conn.cursor()
        agendados = c.execute(
            'SELECT horario FROM agendamentos WHERE barbeiro_id = ? AND data = ? AND status = "agendado"',
            (int(barbeiro_id), data)
        ).fetchall()
        conn.close()
        
        horarios_agendados = [h[0] for h in agendados]
        horarios_livres = [h for h in horarios if h not in horarios_agendados]
        
        return jsonify(horarios_livres)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/agendar', methods=['POST'])
def agendar():
    """Cria um novo agendamento"""
    try:
        dados = request.get_json()
        
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''INSERT INTO agendamentos 
                     (cliente, barbeiro_id, data, horario, servico, valor)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (dados['cliente'], int(dados['barbeiro_id']), dados['data'],
                   dados['horario'], dados['servico'], float(dados['valor'])))
        
        conn.commit()
        conn.close()
        return jsonify({'sucesso': True, 'mensagem': 'Agendamento realizado com sucesso! ✅'})
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro: {str(e)}'}), 400

@app.route('/agenda')
def visualizar_agenda():
    """Página para visualizar a agenda"""
    conn = get_db()
    c = conn.cursor()
    barbeiros = c.execute('SELECT * FROM barbeiros').fetchall()
    conn.close()
    return render_template('agenda.html', barbeiros=barbeiros)

@app.route('/api/agenda/<barbeiro_id>/<data>')
def agenda_barbeiro(barbeiro_id, data):
    """Retorna os agendamentos de um barbeiro para um dia"""
    try:
        conn = get_db()
        c = conn.cursor()
        agendamentos = c.execute(
            '''SELECT a.*, b.nome as barbeiro_nome 
               FROM agendamentos a
               JOIN barbeiros b ON a.barbeiro_id = b.id
               WHERE a.barbeiro_id = ? AND a.data = ? AND a.status = "agendado"
               ORDER BY a.horario''',
            (int(barbeiro_id), data)
        ).fetchall()
        conn.close()
        
        return jsonify([dict(a) for a in agendamentos])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/relatorio')
def relatorio():
    """Página de relatório de vendas"""
    conn = get_db()
    c = conn.cursor()
    relatorio_vendas = c.execute(
        '''SELECT DATE(data) as data, SUM(valor) as total, COUNT(*) as agendamentos
           FROM agendamentos
           WHERE status = "agendado"
           GROUP BY DATE(data)
           ORDER BY data DESC'''
    ).fetchall()
    conn.close()
    
    return render_template('relatorio.html', relatorio=relatorio_vendas)

if __name__ == '__main__':
    print("🔧 Inicializando sistema de agendamento...")
    init_db()
    print("🚀 Servidor iniciando em http://localhost:5000")
    print("📍 Acesse:")
    print("   - Agendamento: http://localhost:5000")
    print("   - Agenda: http://localhost:5000/agenda")
    print("   - Relatório: http://localhost:5000/relatorio")
    print("\n⚠️ Para parar o servidor, pressione CTRL+C\n")
    app.run(debug=True, port=5000)