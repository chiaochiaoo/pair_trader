#############################################################################
# Generated by PAGE version 5.6
#  in conjunction with Tcl version 8.6
#  Nov 10, 2020 10:36:33 PM EST  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    tk_messageBox -title Error -message  "You must open project files from within PAGE."
    exit}


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Relative
}




proc vTclWindow.top44 {base} {
    global vTcl
    if {$base == ""} {
        set base .top44
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background $vTcl(actual_gui_bg) 
    wm focusmodel $top passive
    wm geometry $top 1019x1031+684+259
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 2564 1421
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    vTcl:withBusyCursor {
    labelframe $top.lab52 \
        -font TkDefaultFont -foreground black -text Symbol \
        -background $vTcl(actual_gui_bg) -height 84 -width 870 
    vTcl:DefineAlias "$top.lab52" "Labelframe1" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.lab52
    entry $site_3_0.ent55 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) -insertbackground black -width 154 
    vTcl:DefineAlias "$site_3_0.ent55" "Entry1" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab56 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -text {Input Symbol} 
    vTcl:DefineAlias "$site_3_0.lab56" "Label1" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but57 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Load Symbol} 
    vTcl:DefineAlias "$site_3_0.but57" "Data" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab59 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -text {Status: waiting for symbol} 
    vTcl:DefineAlias "$site_3_0.lab59" "status" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.ent55 \
        -in $site_3_0 -x 0 -relx 0.138 -y 0 -rely 0.476 -width 154 \
        -relwidth 0 -height 17 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab56 \
        -in $site_3_0 -x 0 -relx 0.011 -y 0 -rely 0.476 -width 0 \
        -relwidth 0.12 -height 0 -relheight 0.25 -anchor nw \
        -bordermode ignore 
    place $site_3_0.but57 \
        -in $site_3_0 -x 0 -relx 0.379 -y 0 -rely 0.357 -width 127 \
        -relwidth 0 -height 34 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab59 \
        -in $site_3_0 -x 0 -relx 0.586 -y 0 -rely 0.476 -width 0 \
        -relwidth 0.233 -height 0 -relheight 0.25 -anchor nw \
        -bordermode ignore 
    labelframe $top.lab53 \
        -font TkDefaultFont -foreground black -text {Forecast Setting} \
        -background $vTcl(actual_gui_bg) -height 202 -width 866 
    vTcl:DefineAlias "$top.lab53" "Labelframe2" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.lab53
    radiobutton $site_3_0.rad60 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text Automatic 
    vTcl:DefineAlias "$site_3_0.rad60" "Radiobutton1" vTcl:WidgetProc "Toplevel1" 1
    radiobutton $site_3_0.rad61 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -state normal -text Regressive 
    vTcl:DefineAlias "$site_3_0.rad61" "Radiobutton1_1" vTcl:WidgetProc "Toplevel1" 1
    radiobutton $site_3_0.rad62 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -state normal -text Stationary 
    vTcl:DefineAlias "$site_3_0.rad62" "Radiobutton1_2" vTcl:WidgetProc "Toplevel1" 1
    radiobutton $site_3_0.rad63 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -state normal -text Bullish 
    vTcl:DefineAlias "$site_3_0.rad63" "Radiobutton1_3" vTcl:WidgetProc "Toplevel1" 1
    radiobutton $site_3_0.rad64 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -state normal -text Bearish 
    vTcl:DefineAlias "$site_3_0.rad64" "Radiobutton1_3_1" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but65 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Forecast 
    vTcl:DefineAlias "$site_3_0.but65" "Forecast" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but66 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Chart 
    vTcl:DefineAlias "$site_3_0.but66" "Forecast_1" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent67 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) -insertbackground black \
        -state normal -width 94 
    vTcl:DefineAlias "$site_3_0.ent67" "regressive_input" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent68 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground blue \
        -selectforeground white -width 94 
    vTcl:DefineAlias "$site_3_0.ent68" "bulish_input" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent69 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground blue \
        -selectforeground white -width 94 
    vTcl:DefineAlias "$site_3_0.ent69" "bearish_input" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab70 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) -text Days: 
    vTcl:DefineAlias "$site_3_0.lab70" "Label2" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab71 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Magnitude: 
    vTcl:DefineAlias "$site_3_0.lab71" "Label2_1" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab72 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Magnitude: 
    vTcl:DefineAlias "$site_3_0.lab72" "Label2_1_1" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.rad60 \
        -in $site_3_0 -x 0 -relx 0.104 -y 0 -rely 0.149 -width 0 \
        -relwidth 0.09 -height 0 -relheight 0.144 -anchor nw \
        -bordermode ignore 
    place $site_3_0.rad61 \
        -in $site_3_0 -x 0 -relx 0.104 -y 0 -rely 0.297 -width 0 \
        -relwidth 0.09 -height 0 -relheight 0.144 -anchor nw \
        -bordermode ignore 
    place $site_3_0.rad62 \
        -in $site_3_0 -x 0 -relx 0.104 -y 0 -rely 0.446 -width 0 \
        -relwidth 0.09 -height 0 -relheight 0.153 -anchor nw \
        -bordermode ignore 
    place $site_3_0.rad63 \
        -in $site_3_0 -x 0 -relx 0.081 -y 0 -rely 0.594 -width 0 \
        -relwidth 0.113 -height 0 -relheight 0.134 -anchor nw \
        -bordermode ignore 
    place $site_3_0.rad64 \
        -in $site_3_0 -x 0 -relx 0.092 -y 0 -rely 0.743 -width 0 \
        -relwidth 0.09 -height 0 -relheight 0.134 -anchor nw \
        -bordermode ignore 
    place $site_3_0.but65 \
        -in $site_3_0 -x 0 -relx 0.762 -y 0 -rely 0.198 -width 157 \
        -relwidth 0 -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but66 \
        -in $site_3_0 -x 0 -relx 0.762 -y 0 -rely 0.644 -width 157 \
        -relwidth 0 -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.ent67 \
        -in $site_3_0 -x 0 -relx 0.346 -y 0 -rely 0.347 -width 94 -relwidth 0 \
        -height 17 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.ent68 \
        -in $site_3_0 -x 0 -relx 0.346 -y 0 -rely 0.644 -width 94 -relwidth 0 \
        -height 17 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.ent69 \
        -in $site_3_0 -x 0 -relx 0.346 -y 0 -rely 0.792 -width 94 -relwidth 0 \
        -height 17 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab70 \
        -in $site_3_0 -x 0 -relx 0.277 -y 0 -rely 0.347 -width 0 \
        -relwidth 0.039 -height 0 -relheight 0.104 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab71 \
        -in $site_3_0 -x 0 -relx 0.254 -y 0 -rely 0.644 -width 0 \
        -relwidth 0.084 -height 0 -relheight 0.104 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab72 \
        -in $site_3_0 -x 0 -relx 0.254 -y 0 -rely 0.792 -width 0 \
        -relwidth 0.084 -height 0 -relheight 0.104 -anchor nw \
        -bordermode ignore 
    labelframe $top.lab54 \
        -font TkDefaultFont -foreground black -text {Options } \
        -background $vTcl(actual_gui_bg) -height 617 -width 868 
    vTcl:DefineAlias "$top.lab54" "Labelframe3" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lab52 \
        -in $top -x 0 -relx 0.079 -y 0 -rely 0.039 -width 0 -relwidth 0.854 \
        -height 0 -relheight 0.081 -anchor nw -bordermode ignore 
    place $top.lab53 \
        -in $top -x 0 -relx 0.079 -y 0 -rely 0.155 -width 0 -relwidth 0.85 \
        -height 0 -relheight 0.196 -anchor nw -bordermode ignore 
    place $top.lab54 \
        -in $top -x 0 -relx 0.079 -y 0 -rely 0.369 -width 0 -relwidth 0.852 \
        -height 0 -relheight 0.598 -anchor nw -bordermode ignore 
    } ;# end vTcl:withBusyCursor 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top44 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}
