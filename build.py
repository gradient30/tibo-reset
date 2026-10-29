import json,sys,statistics as st,datetime as dt,html
import os
if not (len(sys.argv)>1 and sys.argv[1]=='render'):
  Z=dt.timezone.utc;BJ=dt.timezone(dt.timedelta(hours=8))
  def P(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00')) if s else None
  def bj(d): return d.astimezone(BJ).strftime('%Y-%m-%d %H:%M') if d else 'unknown'
  X='https://x.com/thsottiaux/status/'
  NOW=dt.datetime.now(Z)
  radar=json.load(open('radar.json'))
  # Detailed events verified via X API (teaser + confirmation); times UTC
  # Radar 'live' entries verified as global resets via X post text (Radar has no observed landing yet)
  LIVE_OK={'2112432076767289678'}
  detail={
   '2107676072871600470':dict(label='Day 2（社区投票）',teaser=('2107578625419866469','2026-10-06T21:07:55Z','Four updates or a reset. Or both. How was day 2.'),pred=None,pred_note='投票决定，无明确时间',conf=('2107676072871600470','2026-10-07T03:35:09Z','…the vote is clear and the community demands a reset… the reset has been processed')),
   '2109132167112782291':dict(label='Day 6',teaser=('2109045392684032299','2026-10-10T22:16:20Z','Day 6/ Reset — Global reset by EOD.'),pred='2026-10-11T07:00:00Z',pred_note='"by EOD"（PDT 当日 24:00）',conf=('2109132167112782291','2026-10-11T04:01:09Z','Put the reset in the bag. All propagated.')),
   '2109812360596865224':dict(label='Day 8',teaser=('2109812360596865224','2026-10-13T01:03:59Z','Day 8/ Reset — Global reset landing by EOD PST time.'),pred='2026-10-13T07:00:00Z',pred_note='"by EOD PST"（按 PDT 当日 24:00）',conf=('2109873287853707513','2026-10-13T05:06:06Z',"What would you like with your side of reset? It's done.")),
   '2110595554036400151':dict(label='Day 10',teaser=('2110595554036400151','2026-10-15T04:56:07Z','Day 10/ Reset — Landing within the next 2 hours'),pred='2026-10-15T06:56:07Z',pred_note='"within the next 2 hours"',conf=None),
   '2111492738025959922':dict(label='Day 13',teaser=('2111492673890824348','2026-10-17T16:20:57Z','Day 13/ Le limit reset — Landing sometime today by EOD PST'),pred='2026-10-18T07:00:00Z',pred_note='"by EOD PST"（按 PDT 当日 24:00）',conf=('2111566005684289735','2026-10-17T21:12:21Z','Done')),
   '2106131810921136451':dict(label='GPT-6.1 Sol 补偿',teaser=('2105843926221660585','2026-10-02T02:14:51Z','Global reset landing tomorrow 10am PST for all paid ChatGPT accounts.'),pred='2026-10-02T17:00:00Z',pred_note='"tomorrow 10am PST"（按 PDT 10:00；字面 PST 则为 18:00Z）',conf=('2106131810921136451','2026-10-02T21:18:48Z','Reset all propagated. Enjoy.')),
   '2103911959544610829':dict(label='短暂中断补偿',teaser=('2103637477760311522','2026-09-26T00:07:13Z',"we're back in action and we'll reset usage limits for all paid users"),pred=None,pred_note='未给时间',conf=('2103911959544610829','2026-09-26T18:17:54Z','Resets all propagated. That will be all.')),
   '2097043464538264003':dict(label='Astra 周',teaser=('2097043464538264003','2026-09-07T19:24:57Z','…We will do a global reset of the usage for all paid subscriptions'),pred=None,pred_note='未给时间',conf=None),
  }
  detail['2112432076767289678']=dict(label='Day 15',teaser=None,pred=None,pred_note='无预告：官宣即重置（所引用的 03:45「Day 15/ We\'re cooked」不是重置预告）',conf=('2112432076767289678','2026-10-20T06:33:48Z',"Day 15/ Nevermind, we're still cooking... and reset. Enjoy."),quoted=('2112268918681485431','2026-10-19T19:45:00Z',"Day 15/ We're cooked（非重置）"))
  ev=[]
  for e in radar['events']:
    if e['type']!='reset' or (e['source']!='archive' and e['id'] not in LIVE_OK): continue
    a=P(e['announced_at']); d=detail.get(e['id'])
    r=dict(id=e['id'],radar_url=e['url'],radar_summary=e['summary'],reasons=e['reason_tags'],
      actual_utc=a.isoformat(),actual_bj=bj(a),actual_basis=('Tibo 官宣帖时间（Radar 已收录该帖，但无实测落地时间）' if e['id'] in LIVE_OK else 'Radar 归档时间（确认帖或实测落地）'),
      window=e['official_window'],label=None,teaser=None,predicted_bj='unknown',pred_note='无独立预告帖记录（多为直接官宣即落地）',lag_teaser_h=None,dev_h=None,confirmation=None)
    if e['official_window'] and e['official_window'].get('end_at'):
      pe=P(e['official_window']['end_at']); r['predicted_bj']=bj(pe)+'（截止）'; r['pred_note']='官方窗口：'+e['official_window']['label']; r['dev_h']=round((a-pe).total_seconds()/3600,2)
    if d:
      r['label']=d['label']
      if d['teaser']:
        t=P(d['teaser'][1]); r['teaser']=dict(url=X+d['teaser'][0],time_bj=bj(t),quote=d['teaser'][2]); r['lag_teaser_h']=round((a-t).total_seconds()/3600,2)
      if d.get('quoted'): r['quoted']=dict(url=X+d['quoted'][0],time_bj=bj(P(d['quoted'][1])),quote=d['quoted'][2])
      r['pred_note']=d['pred_note']
      if d['pred']: pe=P(d['pred']); r['predicted_bj']=bj(pe)+'（截止）'; r['dev_h']=round((a-pe).total_seconds()/3600,2)
      else: r['predicted_bj']='unknown'
      if d['conf']: r['confirmation']=dict(url=X+d['conf'][0],time_bj=bj(P(d['conf'][1])),quote=d['conf'][2])
    ev.append(r)
  ev.sort(key=lambda r:r['actual_utc'])
  for i,r in enumerate(ev):
    r['gap_days']=None if i==0 else round((P(r['actual_utc'])-P(ev[i-1]['actual_utc'])).total_seconds()/86400,2)
  last=P(ev[-1]['actual_utc'])
  def stats(rs):
    g=[r['gap_days'] for r in rs if r['gap_days'] is not None]
    return dict(n=len(g),mean=round(st.mean(g),2),median=round(st.median(g),2),min=min(g),max=max(g))
  r30=[r for r in ev if P(r['actual_utc'])>NOW-dt.timedelta(days=30)]
  s30=stats(r30); sall=stats(ev)
  hrs=[P(r['actual_utc']).astimezone(BJ).hour for r in r30]
  lags=[r['lag_teaser_h'] for r in ev if r['lag_teaser_h'] is not None and r['label'] and r['label'].startswith('Day')]
  since=(NOW-last).total_seconds()/86400
  ch=[r for r in ev if r['label'] and r['label'].startswith('Day')]
  chg=[r['gap_days'] for r in ch[1:]]
  prev=dict(made_bj='2026-10-20 13:21',window_start_bj='2026-10-20 15:00',window_end_bj='2026-10-23 15:00',
    actual_bj=ev[-1]['actual_bj'],actual_basis=ev[-1]['actual_basis'],
    miss_minutes=round((dt.datetime(2026,10,20,7,0,tzinfo=Z)-last).total_seconds()/60,1),
    verdict='未命中：实际重置早于窗口开始约 26 分钟（窗口从 PT Day16 起算，但 Day15 在 PT 当晚 23:33 就重置了）',
    lesson='Day 15 原判为「功能发布日」，但 Tibo 在 PT 当日结束前改成了重置；挑战期内同一天可以从 ship 改判为 reset，窗口应覆盖当前 PT 日的剩余时段。')
  # Day 17: completed (#57). Landed before official deadline 10:00 PDT = BJ 2026-10-23 01:00; user-confirmed 03:05 BJ; no Tibo Done post yet
  teaser_at=P('2026-10-22T06:55:22Z'); reply_at=P('2026-10-22T06:55:54Z'); d17=P('2026-10-22T17:00:00Z')
  r17=dict(id='2113162277688070445',radar_url=X+'2113162277688070445',radar_summary='Day 17 of the 28-day ship-or-reset series: Tibo posted "it\'s reset day today" and replied "Lands tomorrow before 10am PST". Landing confirmed by user quota refresh (2026-10-23 03:05 BJ); no Tibo Done post yet.',reasons=[],
    actual_utc=d17.isoformat(),actual_bj=bj(d17),actual_basis='官方窗口截止（10:00 PDT）前已落地 — 实际时间取上限 01:00 BJ；用户 kien 于 2026-10-23 03:05 BJ 确认额度已刷新；Tibo 尚无 Done 帖',
    window=dict(label='Lands tomorrow before 10am PST',end_at=d17.isoformat()),label='Day 17',
    teaser=dict(url=X+'2113162277688070445',time_bj=bj(teaser_at),quote="Day 17/ Bet you thought we forgot, but no, it's reset day today."),
    reply=dict(url=X+'2113162413008884099',time_bj=bj(reply_at),quote='Lands tomorrow before 10am PST.'),
    predicted_bj=bj(d17)+'（截止）',pred_note='官方窗口：Lands tomorrow before 10am PST（主读 PDT；字面 PST 为 02:00）',
    lag_teaser_h=round((d17-teaser_at).total_seconds()/3600,2),dev_h=0.0,confirmation=None,
    user_confirm=dict(time_bj='2026-10-23 03:05',note='用户 kien 确认额度已刷新（非 Tibo 官方 Done 帖）'),
    gap_days=round((d17-last).total_seconds()/86400,2))
  ev.append(r17); last=d17
  r30=[r for r in ev if P(r['actual_utc'])>NOW-dt.timedelta(days=30)]
  s30=stats(r30); sall=stats(ev)
  hrs=[P(r['actual_utc']).astimezone(BJ).hour for r in r30]
  lagr=[r for r in ev if r['lag_teaser_h'] is not None and r['label'] and r['label'].startswith('Day')]
  lags=[r['lag_teaser_h'] for r in lagr]; lag_labels=[r['label'] for r in lagr]
  since=(NOW-last).total_seconds()/86400
  ch=[r for r in ev if r['label'] and r['label'].startswith('Day')]
  chg=[r['gap_days'] for r in ch[1:]]
  # Day 18: completed (#58). Official window before 10:00 PDT = BJ 2026-10-24 01:00; user-confirmed 08:00 BJ; no Tibo Done post (X checked since reply id)
  d18_teaser_at=P('2026-10-23T04:46:19Z'); d18_reply_at=P('2026-10-23T04:47:34Z'); d18=P('2026-10-23T17:00:00Z')
  r18=dict(id='2113492187770175603',radar_url=X+'2113492187770175603',radar_summary='Day 18 of the 28-day ship-or-reset series: "that\'s a reset!" + reply "Landing tomorrow before 10am PST together with a small ship". Landing confirmed by user quota refresh (2026-10-24 08:00 BJ); no Tibo Done post.',reasons=[],
    actual_utc=d18.isoformat(),actual_bj=bj(d18),actual_basis='官方窗口截止（10:00 PDT）前已落地 — 实际时间取上限 01:00 BJ；用户 kien 于 2026-10-24 08:00 BJ 确认；Tibo 无 Done 帖',
    window=dict(label='Landing tomorrow before 10am PST',end_at=d18.isoformat()),label='Day 18',
    teaser=dict(url=X+'2113492187770175603',time_bj=bj(d18_teaser_at),quote="Day 18/ ... But yes… that's a reset!"),
    reply=dict(url=X+'2113492502355562875',time_bj=bj(d18_reply_at),quote='Landing tomorrow before 10am PST together with a small ship.'),
    predicted_bj=bj(d18)+'（截止）',pred_note='官方窗口：Landing tomorrow before 10am PST（主读 PDT；字面 PST 为 02:00）',
    lag_teaser_h=round((d18-d18_teaser_at).total_seconds()/3600,2),dev_h=0.0,confirmation=None,
    user_confirm=dict(time_bj='2026-10-24 08:00',note='用户 kien 确认已重置（非 Tibo 官方 Done 帖）'),
    gap_days=round((d18-last).total_seconds()/86400,2))
  ev.append(r18); last=d18
  r30=[r for r in ev if P(r['actual_utc'])>NOW-dt.timedelta(days=30)]
  s30=stats(r30); sall=stats(ev)
  hrs=[P(r['actual_utc']).astimezone(BJ).hour for r in r30]
  lagr=[r for r in ev if r['lag_teaser_h'] is not None and r['label'] and r['label'].startswith('Day')]
  lags=[r['lag_teaser_h'] for r in lagr]; lag_labels=[r['label'] for r in lagr]
  since=(NOW-last).total_seconds()/86400
  ch=[r for r in ev if r['label'] and r['label'].startswith('Day')]
  chg=[r['gap_days'] for r in ch[1:]]
  # Day 20 (#59): Done 2026-10-25 14:06 BJ; reply "By midnight PST"; Radar measured ~14:10 BJ
  d20_teaser_at=P('2026-10-25T03:39:31Z'); d20_reply_at=P('2026-10-25T03:40:04Z'); d20_done_at=P('2026-10-25T06:06:16Z'); d20_pred=P('2026-10-25T07:00:00Z')
  r20=dict(id='2114200152701575656',radar_url=X+'2114200152701575656',radar_summary='Day 20 of the 28-day ship-or-reset series: "Rest and reset" + reply "By midnight PST". Done: "It is all propagated." Radar measured landing ~06:10Z.',reasons=[],
    actual_utc=d20_done_at.isoformat(),actual_bj=bj(d20_done_at),actual_basis='Tibo Done 帖时间（It is all propagated）；Radar 实测约 06:10Z / 14:10 BJ',
    window=dict(label='By midnight PST',end_at=d20_pred.isoformat()),label='Day 20',
    teaser=dict(url=X+'2114200152701575656',time_bj=bj(d20_teaser_at),quote='Day 20/ Rest and reset'),
    reply=dict(url=X+'2114200291319124163',time_bj=bj(d20_reply_at),quote='By midnight PST'),
    predicted_bj=bj(d20_pred)+'（截止）',pred_note='官方窗口：By midnight PST（主读 PDT 当日 24:00 = 15:00 BJ）',
    lag_teaser_h=round((d20_done_at-d20_teaser_at).total_seconds()/3600,2),dev_h=round((d20_done_at-d20_pred).total_seconds()/3600,2),
    confirmation=dict(url=X+'2114237083652882932',time_bj=bj(d20_done_at),quote='It is all propagated. Enjoy some mad codexing tomorrow. Fun week ahead too.'),
    gap_days=round((d20_done_at-last).total_seconds()/86400,2))
  ev.append(r20); last=d20_done_at
  # Day 21 (#60): "today is a reset" — no Done; Radar measured landing 14:08 BJ
  d21_teaser_at=P('2026-10-26T05:21:22Z'); d21=P('2026-10-26T06:08:46Z')
  r21=dict(id='2114588174249071102',radar_url=X+'2114588174249071102',radar_summary='Day 21 of the 28-day ship-or-reset series: "Wonder what happens the remaining seven days. But today is a reset." No separate Done post; Radar operator-observed landing 06:08:46Z.',reasons=[],
    actual_utc=d21.isoformat(),actual_bj=bj(d21),actual_basis='Radar 实测落地（operator-observed 06:08:46Z）；Tibo 无独立 Done 帖，预告即当日重置',
    window=None,label='Day 21',
    teaser=dict(url=X+'2114588174249071102',time_bj=bj(d21_teaser_at),quote='Day 21/ Wonder what happens the remaining seven days. But today is a reset.'),
    predicted_bj='unknown',pred_note='无独立时点窗口（「today is a reset」即日落地）',
    lag_teaser_h=round((d21-d21_teaser_at).total_seconds()/3600,2),dev_h=None,confirmation=None,
    gap_days=round((d21-last).total_seconds()/86400,2))
  ev.append(r21); last=d21
  # Day 23 (#61): Done 2026-10-28 14:29 BJ; reply "Lands by midnight PST."
  d23_teaser_at=P('2026-10-28T02:42:53Z'); d23_reply_at=P('2026-10-28T02:43:38Z'); d23_done_at=P('2026-10-28T06:29:38Z'); d23_pred=P('2026-10-28T07:00:00Z')
  r23=dict(id='2115273064481218829',radar_url=X+'2115273064481218829',radar_summary='Day 23 of the 28-day ship-or-reset series: teaser "today is a reset" + reply "Lands by midnight PST." Done: "And it\'s done." Radar measured ~06:35Z.',reasons=['launch'],
    actual_utc=d23_done_at.isoformat(),actual_bj=bj(d23_done_at),actual_basis='Tibo Done 帖时间（And it\'s done. See you tomorrow for some good news.）；Radar 实测约 06:35Z / 14:35 BJ',
    window=dict(label='Lands by midnight PST',end_at=d23_pred.isoformat()),label='Day 23',
    teaser=dict(url=X+'2115273064481218829',time_bj=bj(d23_teaser_at),quote='Day 23/ Much requested iCloud Main & Calendar plugins. Just kidding, today is a reset. Still much requested though!'),
    reply=dict(url=X+'2115273253711409208',time_bj=bj(d23_reply_at),quote='Lands by midnight PST.'),
    predicted_bj=bj(d23_pred)+'（截止）',pred_note='官方窗口：Lands by midnight PST（主读 PDT 当日 24:00 = 15:00 BJ）',
    lag_teaser_h=round((d23_done_at-d23_teaser_at).total_seconds()/3600,2),dev_h=round((d23_done_at-d23_pred).total_seconds()/3600,2),
    confirmation=dict(url=X+'2115330127886463244',time_bj=bj(d23_done_at),quote="And it's done. See you tomorrow for some good news."),
    gap_days=round((d23_done_at-last).total_seconds()/86400,2))
  ev.append(r23); last=d23_done_at
  r30=[r for r in ev if P(r['actual_utc'])>NOW-dt.timedelta(days=30)]
  s30=stats(r30); sall=stats(ev)
  hrs=[P(r['actual_utc']).astimezone(BJ).hour for r in r30]
  lagr=[r for r in ev if r['lag_teaser_h'] is not None and r['label'] and r['label'].startswith('Day')]
  lags=[r['lag_teaser_h'] for r in lagr]; lag_labels=[r['label'] for r in lagr]
  since=(NOW-last).total_seconds()/86400
  ch=[r for r in ev if r['label'] and r['label'].startswith('Day')]
  chg=[r['gap_days'] for r in ch[1:]]
  pending=None
  # Estimate: start = PT-day start containing last + min challenge gap; width 3 days
  PDT=dt.timezone(dt.timedelta(hours=-7))
  t0=(last+dt.timedelta(days=min(chg))).astimezone(PDT).replace(hour=0,minute=0,second=0,microsecond=0)
  t1=t0+dt.timedelta(days=3)
  fc=dict(kind='estimate',window_start_bj=bj(t0),window_end_bj=bj(t1),confidence='低-中',label='估计（非官方）',
    basis='估计，非官方。挑战期已兑现 '+'/'.join(r['label'].replace('Day ','').replace('（社区投票）','') for r in ch)+'，间隔 '+'/'.join(str(g) for g in chg)+' 天（中位 '+str(round(st.median(chg),2))+'，最短 '+str(min(chg))+'）；近 30 天中位 '+str(s30['median'])+' 天。最近 Day23 于 '+bj(last)+' 落地（Tibo Done；Radar 实测约 14:35 BJ）。Day19/22/24 为产品 ship，非重置；Day20/21 亦为全局重置。窗口起点＝上次＋最短间隔所在 PT 日开始，宽 3 天。',
    change='出现「Day N/ Reset」帖 → 改为官方窗口；若更早重置，本窗口提前失效；窗口过去仍无帖则撤回，不顺延。',
    hour_note='近 30 天落地时刻（北京）：'+str(sorted(hrs))+' — 多在 12–15 点或 01 点前后（Pacific 上午），不给固定时点',
    sources=['https://x.com/thsottiaux','https://codex-reset.com'])
  estimate_superseded=dict(made_bj='2026-10-24 08:01',window_start_bj='2026-10-24 15:00',window_end_bj='2026-10-27 15:00',
    verdict='命中：Day20 于 2026-10-25 14:06 BJ 落地，位于该估计窗口内；随后 Day21/23 继续重置',confidence='低-中',
    prior_hit=dict(made_bj='2026-10-21 09:58',window_start_bj='2026-10-21 15:00',window_end_bj='2026-10-24 15:00',
      verdict='命中：Day17 于 2026-10-23 01:00 BJ 前落地，位于该估计窗口内（期间被官方预告取代）',confidence='低-中'))
  data=dict(generated_at_bj=bj(NOW),sources=['https://x.com/thsottiaux','https://codex-reset.com/api/timeline','https://status.openai.com'],
   last_reset=ev[-1],days_since_last=round(since,2),stats_30d=s30,stats_all=sall,teaser_lag_hours_challenge=lags,teaser_lag_labels=lag_labels,forecast=fc,forecast_check=prev,estimate_superseded=estimate_superseded,pending=pending,events=ev,
   gaps=['status.openai.com 未纳入（仅作故障线；本页核对时 All Systems Operational）','多数早期事件只有确认/官宣时间，无独立预告帖，预测时间=unknown','Day 10 未在 X 找到 Tibo 完成帖；实际时间取 Radar 实测 06:13Z','Radar 归档的 Day 8/10/13 时间为 Radar 实测落地时间，非确认帖时间','2026-03-04 的事件仅覆盖约 9% 用户，Radar 仍记为 reset，保留','静默重置仅 2026-08-25 一次被 Radar 收录；其他静默重置未知','banked reset 单独列出，不计入间隔','Day 15（10-20）实际时间取官宣帖时间','2026-10-21 01:10 的 credits 补偿帖（约 4 万账户账单限额错误）不是全局重置，未计入次数','Day 17 已计入 #57：官方窗口上限 01:00 BJ＋用户确认；Radar 后补实测约 01:10 BJ','Day 18 已计入 #58：官方窗口上限 01:00 BJ＋用户确认；Radar 后补实测约 01:40 BJ','Day 20 已计入 #59：Tibo Done 14:06 BJ（Radar 实测约 14:10 BJ）；窗口 midnight PST','Day 21 已计入 #60：无 Done 帖，取 Radar 实测 14:08 BJ；预告「today is a reset」','Day 22/24 为产品更新（Terra / Text your dot），非重置','Day 23 已计入 #61：Tibo Done 14:29 BJ（Radar 实测约 14:35 BJ）；窗口 midnight PST'],
   banked=[dict(date_bj=bj(P(e['announced_at'])),summary=e['summary'],url=e['url']) for e in radar['events'] if e['type']=='credits'],
   non_reset=[dict(date_bj='2026-10-21 01:10',kind='credits_compensation',summary='约 4 万账户周末账单限额配置错误已修复；受影响用户获 credits 补偿。这不是全局重置。',url='https://x.com/thsottiaux/status/2112592264686149749'),
              dict(date_bj='2026-10-23 12:47',kind='product_ship_teaser',summary='Day18 回复中的「small ship」指同日小产品发布，不是 credits/banked 额度包；Day18 重置已于 10-24 01:00 BJ 前落地。',url='https://x.com/thsottiaux/status/2113492502355562875'),
              dict(date_bj='2026-10-24 07:12',kind='product_ship',summary='Day19/ Small updates（dots 通话、推理切换不失效缓存、codex cli 更新）——ship 日，非重置。',url='https://x.com/thsottiaux/status/2113770573994299544'),
              dict(date_bj='2026-10-27 03:24',kind='product_ship',summary='Day22/ Terra is back（GPT-6.1 Terra 模型发布）——ship 日，非重置。',url='https://x.com/thsottiaux/status/2114800277677092936'),
              dict(date_bj='2026-10-29 09:49',kind='product_ship',summary='Day24/ Text your dot（iMessage/RCS 文本你的 dot）——产品更新，非重置。',url='https://x.com/thsottiaux/status/2115622002581188681')])
  json.dump(data,open('data.json','w'),ensure_ascii=False,indent=1)
  print(s30,sall,lags,fc,len(ev))
d=open('data.json').read();open('index.html','w').write(open('tpl.html').read().replace('__DATA__',d));print('rendered index.html')
