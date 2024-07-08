# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FleetWorkOrderAnalysis(models.Model):
    _name = "fleet_work_order_analysis"
    _description = "Fleet Work Order Analysis"
    _order = "vehicle_id, driver_id"
    _auto = False
    _rec_name = "vehicle_id"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="fleet_work_order_type",
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet_vehicle",
    )
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
    )
    codriver_id = fields.Many2one(
        string="Co-Driver",
        comodel_name="res.partner",
    )
    date_start = fields.Datetime(
        string="ETD",
    )
    date_end = fields.Datetime(
        string="ETA",
    )
    real_date_depart = fields.Datetime(
        string="RTD",
    )
    real_date_arrive = fields.Datetime(
        string="RTA",
    )
    odometer = fields.Float(
        string="Odoometer",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("ready", "Ready to Start"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
    )

    @property
    def _table_query(self):
        return "%s %s %s %s" % (
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
        )

    @api.model
    def _select(self):
        select_str = """
             SELECT
                 row_number() OVER() as id,
                 w.type_id AS type_id,
                 w.vehicle_id AS vehicle_id,
                 w.driver_id AS driver_id,
                 w.codriver_id AS codriver_id,
                 w.estimated_date_depart AS date_start,
                 w.estimated_date_arrive AS date_end,
                 w.real_date_depart AS real_date_depart,
                 w.real_date_arrive AS real_date_arrive,
                 w.state AS state,
                 SUM(w.end_odometer - w.start_odometer) AS odometer
        """
        return select_str

    @api.model
    def _from(self):
        from_str = """
            FROM
                fleet_work_order AS w
        """
        return from_str

    @api.model
    def _where(self):
        where_str = """

        """
        return where_str

    @api.model
    def _group_by(self):
        group_by_str = """
            GROUP BY
                w.type_id,
                w.vehicle_id,
                w.driver_id,
                w.codriver_id,
                w.estimated_date_depart,
                w.estimated_date_arrive,
                w.real_date_depart,
                w.real_date_arrive,
                w.state
        """
        return group_by_str
