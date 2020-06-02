def migrate(cr, installed_version):
    cr.execute("""
        UPDATE ir_model_data
        SET module = 'crnd_wsd'
        WHERE module = 'crnd_wsd_kind'
          AND model IN (
                 'ir.model.fields',
                 'ir.model.constraint',
                 'ir.model.relation',
                 'ir.ui.menu',
                 'ir.model.access',
                 'ir.actions.act_window',
                 'request.kind');

        -- Delete views
        DELETE FROM ir_ui_view WHERE id IN (
            SELECT res_id
            FROM ir_model_data
            WHERE model = 'ir.ui.view'
              AND module = 'crnd_wsd_kind'
        );

        -- DELETE references to ir_model
        DELETE FROM ir_model_data
        WHERE model = 'ir.model'
          AND module = 'crnd_wsd_kind';

        -- Delete constraints
        DELETE FROM ir_model_constraint WHERE module = (
            SELECT id
            FROM ir_module_module
            WHERE name = 'crnd_wsd_kind'
        );

        -- DELETE removed modules from database
        DELETE FROM ir_module_module WHERE name = 'crnd_wsd_kind';
    """)
