CREATE OR REPLACE FUNCTION update_dttm_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.update_dttm = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_backlog_update_dttm BEFORE UPDATE 
	ON backlog FOR EACH ROW EXECUTE PROCEDURE 
	update_dttm_column();
