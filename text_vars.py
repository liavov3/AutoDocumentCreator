def make_it_hebrew(text: str):
    s = text.split()[::-1]
    l = []
    for i in s:
        l.append(i)
    return(" ".join(l))


new_line = '\n'

tab_number_header = 'מספר המסמך'
tab_name_header = 'שם המסמך'
tab_date_header = 'תאריך'
tab_shamur_header = 'סיווג: שמור'
tab_logo = ''

tab_shamur_contex = 'יופץ עותק דיגיטלי בלבד'

tab_downder = 'יחידת נס"א/ ענף חני"ת/ מדור חימוש מונחה'

title_lists = "results "

# title_FirstShot = "first shot: " #after the dash you should put the naame of the experiment
# title_SecondShot = "second shot:"
# title_ThirdShot = "Third shot: "
# title_FourthShot = "Fourth shot:- "
title_FirstShot = "ירי ראשון אדום 1- " #after the dash you should put the naame of the experiment
title_SecondShot = "ירי שני אדום 2- "
title_ThirdShot = "ירי שלישי אדום 3- "
title_FourthShot = "ירי רביעי אדום 4- "


# experiment_top_view_text = "1) Missile trajectory - Top view"
experiment_top_view_text = " מסלול מעוף ממבט על במערכת צירים מקומית - משגר בראשית הצירים"
experiment_alt_time_text = "גובה לזמן במערכת צירים מקומית "
experiment_traj_text = f' טריאנגולצית קרנ"צים'

spatial_error_distribution_telemetry_text = " התפלגות שגיאות מרחביות ביחס לנתוני הטלמטריה"
spatial_error_distribution_to_traj_weibel_text = f'התפלגות שגיאות מרחביות בין מכ"ם lebieW לנתוני הטריאנגולציה האופטית '
spatial_error_distribution_average_text = f" התקבלה התפלגות של שגיאה מרחבית ממוצעת של "  #after that there is the real spatial error
angle_errors_distributions_average_text = f"התקבלו התפלגות של שגיאה זוויתיות ממוצעות: "  #after that there is the real spatial error
standart_devision_text = "עם סטיית תקן ממוצעת:"  #after that there is the real standart_devision

spetial_error_azimuth_formula_txt = 'שגיאה מרחבית אזימוט:'
spetial_error_elevation_formula_txt = 'שגיאה מרחבית אלביישן:'

weibel_text = f'מכם lebieW'

worked_bad_text = ' לא פעל בתרחיש אדום 1 בצורה תקינה'
worked_good_text = f'''
בתרחיש זה כל אמצעי האיכון פעלו באופן תקין והסכימו זה עם זה במסגרת
השגיאות המרחביות המוכרות מניסויי עבר.
'''

napar_title_text = f'ניתוח נפ"ר'
napar_top_view_text = f' גרף נפ"ר ממבט על במערכת צירים UTM36R'

can_see_till_sec_text = 'ניתן לראות כי עד שניה'
napar_close_look_text = f' במבט מקורב לאזור המטרה:'
napar_moving_to_text = f'כפי שניתן לראות הטלמטריה )GPS )נותנת נפ"ר יציב, אשר נע לכיוון'

napar_optic_conclusion_text =f''' בנוסף ניתן להבחין כי האופטיקה מתכנסת גם היא לאזור הפגיעה הסופי,  
בהתאמה עם הטלמטריה, אך בריצוד רחב יותר לאור שגיאות מיקום והערכת 
המהירות גדולות יותר.
'''

napar_no_GPS_text = f'בהיעדר נתוני טלמטריה (GPS), לא חושב נפ"ר המסתמך על איכון GPS.'


closr_look_to_target_text = ' במבט מקורב לאזור המטרה:'


valid_text = 'כמות הזמן שכל תחנה עקבה אחריי הטיל:'

day_fire = 'ירי יום'
scenrio_fire = 'אדום'


spetial_error_formula_txt = "התקבלה התפלגות של שגיאה מרחבית:"
standart_devision_text = "עם סטיית תקן: "  #after that there is the real standart_devision

