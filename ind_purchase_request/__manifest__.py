{
    "name": "Indomin Purchase Request",
    "author": "Javier Yataco",
    "version": "15.0.1.1.0",
    "summary": "Cambios aplicados para el módulo Purchase Request ",
    "category": "Purchase Management",
    "depends": ["purchase", "purchase_request","report_xlsx","account"],
    "data": [
        'security/res_group.xml',
        "security/purchase_request_security.xml",
        "security/purchase_order_security.xml",
        "security/ir.model.access.xml",
        "reports/report_purchase_request.xml",
        "reports/purchase_order_report.xml",
        "reporte_rfq/reporte_rfq.xml",
        "views/purchase_request_view.xml",
        "views/purchase_request_report.xml",
        "views/purchase_order_view.xml",
        "views/purchase_request_line_view.xml",
        "views/purchase_order_line_view.xml",
        "views/res_users_views.xml",
        "views/update_exchange_rate.xml",
        "wizard/purchase_request_line_make_purchase_order.xml",
    ],
    "demo": [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
