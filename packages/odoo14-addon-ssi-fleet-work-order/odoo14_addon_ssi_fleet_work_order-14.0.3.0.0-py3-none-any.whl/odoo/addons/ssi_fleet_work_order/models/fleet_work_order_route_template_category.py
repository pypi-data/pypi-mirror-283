# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class FleetWorkOrderRouteTemplateCategory(models.Model):
    _name = "fleet_work_order_route_template_category"
    _description = "Fleet Work Order Route Template Category"
    _inherit = ["mixin.master_data"]
