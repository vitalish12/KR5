keyword = '%Python%'

-- получает список всех компаний и количество вакансий у каждой компании
sql1 = '''SELECT DISTINCT employer_name, COUNT(*) AS count_vacancies
    FROM employers
    GROUP BY employer_name
    ORDER BY count_vacancies DESC'''

-- получает список всех вакансий с указанием названи€ компании, названи€ вакансии и зарплаты и ссылки на вакансию
sql2 = '''SELECT employer_name, vacancy_name, salary_from, salary_to, currency, url
    FROM employers
    ORDER BY employer_name'''

-- получает среднюю зарплату по ваканси€м
sql3 = '''SELECT ROUND(AVG(salary_to + salary_from / 2)) AS avg_salary
    FROM employers
    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL'''

-- получает список всех вакансий, у которых зарплата выше средней по всем ваканси€м
sql4 = '''SELECT vacancy_name
    FROM employers
    WHERE (salary_to + salary_from) / 2 > (SELECT AVG(salary_to + salary_from / 2) FROM employers WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL)'''


-- получает список всех вакансий, в названии которых содержатс€ переданные в метод слова, например УpythonФ
sql5 = f'''SELECT vacancy_name, url
    FROM employers
    WHERE vacancy_name ILIKE '%{keyword}%'
    '''