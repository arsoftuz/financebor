// Telegram WebApp obyektini olish
const tg = window.Telegram.WebApp;

// WebApp-ni ishga tushirish
tg.expand();

// Til ma'lumotlari
const translations = {
    uz: {
        title: "Moliya Hisobotlari",
        day: "Kun",
        week: "Hafta",
        month: "Oy",
        year: "Yil",
        all: "Hammasi",
        income: "Daromad",
        expense: "Xarajat",
        balance: "Balans",
        expenses: "Xarajatlar",
        incomes: "Daromadlar",
        recent_transactions: "So'nggi tranzaksiyalar",
        no_transactions: "Tranzaksiyalar mavjud emas",
        sum: "so'm"
    },
    ru: {
        title: "Финансовые отчеты",
        day: "День",
        week: "Неделя",
        month: "Месяц",
        year: "Год",
        all: "Все",
        income: "Доход",
        expense: "Расход",
        balance: "Баланс",
        expenses: "Расходы",
        incomes: "Доходы",
        recent_transactions: "Последние транзакции",
        no_transactions: "Транзакции отсутствуют",
        sum: "сум"
    }
};

// Joriy til
let currentLang = tg.initDataUnsafe?.user?.language_code || 'uz';
if (!translations[currentLang]) {
    currentLang = 'uz'; // Standart til
}

// Joriy davr
let currentPeriod = 'month';

// Sahifani tarjima qilish
function translatePage() {
    const t = translations[currentLang];
    
    // Sarlavha
    document.querySelector('h1').textContent = t.title;
    document.title = t.title;
    
    // Davr tugmalari
    document.querySelector('[data-period="day"]').textContent = t.day;
    document.querySelector('[data-period="week"]').textContent = t.week;
    document.querySelector('[data-period="month"]').textContent = t.month;
    document.querySelector('[data-period="year"]').textContent = t.year;
    document.querySelector('[data-period="all"]').textContent = t.all;
    
    // Umumiy ma'lumotlar
    document.querySelector('.income h3').textContent = t.income;
    document.querySelector('.expense h3').textContent = t.expense;
    document.querySelector('.balance h3').textContent = t.balance;
    
    // Diagrammalar
    document.querySelector('.chart-box:nth-child(1) h3').textContent = t.expenses;
    document.querySelector('.chart-box:nth-child(2) h3').textContent = t.incomes;
    
    // Tranzaksiyalar
    document.querySelector('.transactions-list h3').textContent = t.recent_transactions;
}

// Raqamni formatlash
function formatNumber(number) {
    return new Intl.NumberFormat(currentLang === 'uz' ? 'uz-UZ' : 'ru-RU').format(number);
}

// Ma'lumotlarni yuklash
async function loadData() {
    try {
        // Telegram WebApp orqali ma'lumotlarni olish
        tg.MainButton.setText('Yuklanmoqda...');
        tg.MainButton.show();
        tg.MainButton.disable();
        
        // Ma'lumotlarni olish uchun so'rov yuborish
        const userData = tg.initDataUnsafe;
        const userId = userData?.user?.id;
        
        // Botga so'rov yuborish
        tg.sendData(JSON.stringify({
            action: 'get_report',
            period: currentPeriod,
            user_id: userId
        }));
        
        // Botdan ma'lumotlarni olish
        tg.onEvent('mainButtonClicked', function() {
            // Bu yerda bot ma'lumotlarni qayta yuboradi
            tg.close();
        });
        
        // Test uchun namuna ma'lumotlar
        const sampleData = getSampleData();
        updateUI(sampleData);
        
        tg.MainButton.setText('Yopish');
        tg.MainButton.enable();
    } catch (error) {
        console.error('Ma\'lumotlarni yuklashda xatolik:', error);
    }
}

// Test uchun namuna ma'lumotlar
function getSampleData() {
    return {
        total_income: 5000000,
        total_expense: 3500000,
        balance: 1500000,
        expense_by_category: [
            { name: "Oziq-ovqat", amount: 1200000 },
            { name: "Transport", amount: 800000 },
            { name: "Kommunal", amount: 600000 },
            { name: "Ko'ngil ochar", amount: 500000 },
            { name: "Boshqa", amount: 400000 }
        ],
        income_by_category: [
            { name: "Ish haqi", amount: 4000000 },
            { name: "Qo'shimcha daromad", amount: 1000000 }
        ],
        recent_transactions: [
            { id: 1, category: "Oziq-ovqat", amount: 150000, type: "expense", description: "Supermarket", date: "2023-08-07" },
            { id: 2, category: "Ish haqi", amount: 4000000, type: "income", description: "Oylik", date: "2023-08-05" },
            { id: 3, category: "Transport", amount: 50000, type: "expense", description: "Taksi", date: "2023-08-04" }
        ]
    };
}

// UI-ni yangilash
function updateUI(data) {
    const t = translations[currentLang];
    
    // Umumiy ma'lumotlarni ko'rsatish
    document.getElementById('total-income').textContent = formatNumber(data.total_income) + ' ' + t.sum;
    document.getElementById('total-expense').textContent = formatNumber(data.total_expense) + ' ' + t.sum;
    document.getElementById('balance').textContent = formatNumber(data.balance) + ' ' + t.sum;
    
    // Xarajatlar diagrammasini yaratish
    createPieChart('expense-chart', 'expense-legend', data.expense_by_category);
    
    // Daromadlar diagrammasini yaratish
    createPieChart('income-chart', 'income-legend', data.income_by_category);
    
    // Tranzaksiyalarni ko'rsatish
    displayTransactions(data.recent_transactions);
}

// Diagramma yaratish
function createPieChart(chartId, legendId, data) {
    const chartContainer = document.getElementById(chartId);
    const legendContainer = document.getElementById(legendId);
    
    // Eski diagrammani tozalash
    chartContainer.innerHTML = '';
    legendContainer.innerHTML = '';
    
    if (!data || data.length === 0) {
        chartContainer.innerHTML = `<p class="no-data">${translations[currentLang].no_transactions}</p>`;
        return;
    }
    
    // Canvas yaratish
    const canvas = document.createElement('canvas');
    chartContainer.appendChild(canvas);
    
    // Ranglar
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#8AC249', '#EA80FC', '#00E5FF', '#FF5252'
    ];
    
    // Ma'lumotlarni tayyorlash
    const labels = data.map(item => item.name);
    const values = data.map(item => item.amount);
    const backgroundColors = data.map((_, i) => colors[i % colors.length]);
    
    // Diagramma yaratish
    new Chart(canvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    // Legendani yaratish
    data.forEach((item, i) => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        
        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color';
        colorBox.style.backgroundColor = colors[i % colors.length];
        
        const label = document.createElement('span');
        label.textContent = `${item.name}: ${formatNumber(item.amount)} ${translations[currentLang].sum}`;
        
        legendItem.appendChild(colorBox);
        legendItem.appendChild(label);
        legendContainer.appendChild(legendItem);
    });
}

// Tranzaksiyalarni ko'rsatish
function displayTransactions(transactions) {
    const container = document.getElementById('transactions-container');
    container.innerHTML = '';
    
    if (!transactions || transactions.length === 0) {
        container.innerHTML = `<p class="no-data">${translations[currentLang].no_transactions}</p>`;
        return;
    }
    
    transactions.forEach(transaction => {
        const item = document.createElement('div');
        item.className = 'transaction-item';
        
        const info = document.createElement('div');
        info.className = 'transaction-info';
        
        const category = document.createElement('div');
        category.className = 'transaction-category';
        category.textContent = transaction.category;
        
        const description = document.createElement('div');
        description.className = 'transaction-description';
        description.textContent = `${transaction.description} • ${transaction.date}`;
        
        info.appendChild(category);
        info.appendChild(description);
        
        const amount = document.createElement('div');
        amount.className = `transaction-amount ${transaction.type}`;
        const sign = transaction.type === 'income' ? '+' : '-';
        amount.textContent = `${sign} ${formatNumber(transaction.amount)} ${translations[currentLang].sum}`;
        
        item.appendChild(info);
        item.appendChild(amount);
        container.appendChild(item);
    });
}

// Davr tugmalarini boshqarish
document.querySelectorAll('.period-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Faol tugmani o'zgartirish
        document.querySelector('.period-btn.active').classList.remove('active');
        button.classList.add('active');
        
        // Davrni o'zgartirish va ma'lumotlarni qayta yuklash
        currentPeriod = button.getAttribute('data-period');
        loadData();
    });
});

// Sahifa yuklanganda
document.addEventListener('DOMContentLoaded', () => {
    // Sahifani tarjima qilish
    translatePage();
    
    // Ma'lumotlarni yuklash
    loadData();
});
