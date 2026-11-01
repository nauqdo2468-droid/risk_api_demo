import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import calculate_loan_to_income


def hello(request):
    name = request.GET.get("name", "bạn")

    return JsonResponse(
        {
            "status": "success",
            "data": {
                "message": f"Xin chào, {name}!"
            }
        },
        json_dumps_params={"ensure_ascii": False}
    )


def risk_demo(request):
    income_text = request.GET.get("income")
    loan_text = request.GET.get("loan")

    if income_text is None or loan_text is None:
        return JsonResponse(
            {
                "status": "error",
                "message": "Cần cung cấp income và loan."
            },
            status=400,
            json_dumps_params={"ensure_ascii": False}
        )

    try:
        income = float(income_text)
        loan = float(loan_text)
    except ValueError:
        return JsonResponse(
            {
                "status": "error",
                "message": "Thu nhập và số tiền vay phải là số."
            },
            status=400,
            json_dumps_params={"ensure_ascii": False}
        )

    try:
        ratio = calculate_loan_to_income(income, loan)
    except ValueError as e:
        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status=400,
            json_dumps_params={"ensure_ascii": False}
        )

    return JsonResponse({
        "status": "success",
        "data": {
            "income": income,
            "loan": loan,
            "loan_to_income_ratio": ratio
        }
    })

@csrf_exempt
def loan_applications(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Chỉ chấp nhận phương thức POST."
            },
            status=405
        )

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "JSON không hợp lệ."
            },
            status=400
        )

    return JsonResponse(
        {
            "status": "success",
            "data": data
        },
        json_dumps_params={"ensure_ascii": False}
    )
