def migrate(cr, installed_version):
    cr.execute("""
        UPDATE ir_model_data
        SET module = 'generic_request'
        WHERE module = 'generic_request_priority'
          AND model IN (
                 'ir.model.fields',
                 'ir.model.constraint',
                 'ir.model.relation',
                 'ir.ui.menu',
                 'ir.model.access',
                 'ir.actions.act_window');

        -- Move all request-related data to 'generic_request' namespace
        UPDATE ir_model_data
        SET module = 'generic_request'
        WHERE module = 'generic_request_priority'
          AND model LIKE 'request.%';

        -- Delete views
        DELETE FROM ir_ui_view WHERE id IN (
            SELECT res_id
            FROM ir_model_data
            WHERE model = 'ir.ui.view'
              AND module = 'generic_request_priority'
        );

        -- Delete constraints
        DELETE FROM ir_model_constraint WHERE module = (
            SELECT id
            FROM ir_module_module
            WHERE name = 'generic_request_priority'
        );

        -- DELETE references to ir_model
        DELETE FROM ir_model_data
        WHERE model = 'ir.model'
          AND module = 'generic_request_priority';

        -- DELETE removed modules from database
        DELETE FROM ir_module_module WHERE name = 'generic_request_priority';
    """)
