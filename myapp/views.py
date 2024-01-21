from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from django.shortcuts import render
from .forms import EmployeeForm


def create_users():
    user = User.objects.create_user(username='claudiu', email='claudiu@gmail.com', password='receptionist')
    user.first_name = 'First'
    user.last_name = 'Last'
    user.save()

def page1(request):
    return render(request, 'page1.html')

def page2(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            return render(request, 'page2.html', {'form': form, 'success_message': 'Form submitted successfully!'})
    else:
        form = EmployeeForm()

    return render(request, 'page2.html', {'form': form})

def find_patient(request):
    patient_id = request.GET.get('patient_id', '')
    cnp = request.GET.get('cnp', '')

    if not( patient_id or cnp ):
        print("No fields filled in!")
        return JsonResponse({'success': False, 'error': "Please fill in at least one field."})    

    try:
        if patient_id:
            query = f"SELECT appointments.appoint_ID AS Appointment_ID, pacients.p_surname AS Pacient_Surname,pacients.p_name AS Pacient_Name,   pacients.CNP AS CNP, employees.e_surname AS Employee_Surname, employees.e_name AS Employee_Name, doctors.specialization AS specialization, appointments.room_no AS Room_Number FROM pacients JOIN appointments ON pacients.account_ID = appointments.account_ID JOIN doctors ON appointments.seal = doctors.seal JOIN employees ON doctors.employee_ID = employees.employee_ID WHERE pacients.pacient_ID = '{patient_id}';"
        else:
            query = f"SELECT appointments.appoint_ID AS Appointment_ID, pacients.p_surname AS Pacient_Surname,pacients.p_name AS Pacient_Name,   pacients.CNP AS CNP, employees.e_surname AS Employee_Surname, employees.e_name AS Employee_Name, doctors.specialization AS specialization, appointments.room_no AS Room_Number FROM pacients JOIN appointments ON pacients.account_ID = appointments.account_ID JOIN doctors ON appointments.seal = doctors.seal JOIN employees ON doctors.employee_ID = employees.employee_ID WHERE pacients.CNP = '{cnp}';"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if results:
            data = [{'field1': result[0], 'field2': result[1], 'field3': result[2], 'field4': result[3], 'field5': result[4],'field6': result[5], 'field7': result[6], 'field8': result[7]} for result in results]
            return JsonResponse({'success': True, 'data': data, 'query_output': f"Matches found: {len(results)}"})
        else:
            return JsonResponse({'success': False, 'error': 'No matching records found.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('page2')
            else:
                return redirect('page1')
        else:
                        return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')


def submit_employee_form(request):
    success_message = None

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():

            employee_ID = form.cleaned_data['employee_ID']
            CNP = form.cleaned_data['CNP']
            DOB = form.cleaned_data['DOB']
            phone_no = form.cleaned_data['phone_no']
            e_name = form.cleaned_data['e_name']
            e_surname = form.cleaned_data['e_surname']
            role = form.cleaned_data['role']
            DOE = form.cleaned_data['DOE']

            dob_str = str(form.cleaned_data['DOB'])
            dob_str = dob_str[:-6]
            doe_str = str(form.cleaned_data['DOE'])
            doe_str = doe_str[:-6]

            sql = f"""
                INSERT INTO employees (employee_ID, CNP, DOB, phone_no, e_name, e_surname, role, DOE)
                VALUES ('{employee_ID}', '{CNP}', '{dob_str}', '{phone_no}', '{e_name}', '{e_surname}', '{role}', '{doe_str}');
            """

            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)

                success_message = 'Employee data has been successfully submitted.'
                form = EmployeeForm()

            except Exception as e:
                print(str(e))
                return render(request, 'page2.html', {'form': form, 'error_message': f'Error: {str(e)}'})

        else:
            return render(request, 'page2.html', {'form': form})


    return render(request, 'page2.html', {'form': form, 'success_message': success_message})


def show_query_result(request):
    query = "SELECT * FROM employees;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    employee_fields = ['employee_ID', 'CNP', 'DOB', 'phone_no', 'e_name', 'e_surname', 'role', 'DOE']

    query_result = [dict(zip(employee_fields, result)) for result in results]
  
    return render(request, 'page2.html', {'query_result': query_result})