create trigger FirstUpper_tgr 
       after insert on StationInfo
       begin
            insert into StationInfo(StationNameEn, StationNameCh, Longitude, Latitude)
            select 
            upper(substr(new.StationNameEn,1,1))||substr(new.StationNameEn,2),
            new.StationNameCh,
            new.Longitude,
            new.Latitude;
       end;
create trigger FirstUpper_tgr 
       after insert on StationInfo
       begin
            update StationInfo set 
	StationNameEn = upper(substr(new.StationNameEn,1,1))||substr(new.StationNameEn,2)
 	where 
	StationNameEn == new.StationNameEn;
		
       end;

create trigger routeinfo_tgr1 
       after insert on RouteInfo
       begin
            update RouteInfo set 
	CurrentStationEn = upper(substr(new.CurrentStationEn,1,1))||substr(new.CurrentStationEn,2)
 	where 
	CurrentStationEn == new.CurrentStationEn;
		
       end;

create trigger routeinfo_tgr2
       after update on RouteInfo
       begin
            update RouteInfo set 
	CurrentStationEn = upper(substr(new.CurrentStationEn,1,1))||substr(new.CurrentStationEn,2)
 	where 
	CurrentStationEn == new.CurrentStationEn;
		
       end;