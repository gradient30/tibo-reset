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
  # Day 18 official teaser (preview only — not a completed reset; Day17 remains #57)
  d18_teaser_at=P('2026-10-23T04:46:19Z'); d18_reply_at=P('2026-10-23T04:47:34Z')
  # Same Day17 PDT convention: post BJ 12:46 = PDT Oct22 evening → Pacific tomorrow = Oct23 PDT
  # before 10:00 PDT (UTC-7) = 17:00Z = BJ 2026-10-24 01:00; literal PST (UTC-8) = 18:00Z = BJ 02:00
  d18_deadline=P('2026-10-23T17:00:00Z'); d18_deadline_pst=P('2026-10-23T18:00:00Z')
  pending=dict(
    id='2113492187770175603',label='Day 18',status='pending',
    teaser=dict(url=X+'2113492187770175603',time_bj=bj(d18_teaser_at),time_utc=d18_teaser_at.isoformat(),
      quote="Day 18/ Decisions API is GA, OpenResponses joined the Linux Foundation, we shipped some performance improvements and Uber is going all-in on codex & work. But yes… that's a reset!"),
    reply=dict(url=X+'2113492502355562875',time_bj=bj(d18_reply_at),time_utc=d18_reply_at.isoformat(),
      quote='Landing tomorrow before 10am PST together with a small ship.'),
    predicted_bj='2026-10-24 01:00 前（PDT）',
    predicted_bj_alt='2026-10-24 02:00 前（字面 PST）',
    predicted_utc=d18_deadline.isoformat(),
    pred_note='官方窗口：Landing tomorrow before 10am PST（主读 PDT；字面 PST 晚 1 小时）；「small ship」= 同日小产品发布，非 credits/banked',
    actual_bj='unknown',actual_basis='尚未落地 — 等待 Tibo Done / Radar 实测 / 用户确认',
    radar_urls=[X+'2113492187770175603',X+'2113492502355562875'],
    radar_note='Radar live 已收录预告帖与回复，confirmed=false')
  fc=dict(
    kind='official',
    window_start_bj=bj(max(NOW,d18_teaser_at)),
    window_end_bj='2026-10-24 01:00',
    window_end_bj_alt='2026-10-24 02:00',
    confidence='高',
    label='官方预告窗口',
    basis='Tibo 官方预告：主帖 Day 18「that\'s a reset!」（'+bj(d18_teaser_at)+'）+ 回复「Landing tomorrow before 10am PST together with a small ship.」（'+bj(d18_reply_at)+'）。发帖时刻约为 PDT 10-22 晚 / 北京 10-23 中午，故 Pacific「tomorrow」= 10-23 PDT 上午；before 10:00 PDT（UTC−7）= 2026-10-23 17:00Z = 北京时间 2026-10-24 01:00 前。字面按 PST（UTC−8）则晚 1 小时至 02:00。「small ship」指同日小产品发布，不是 credits/banked 额度包。最近已完成全局重置仍为 Day17（'+ev[-1]['actual_bj']+'，#57；用户 10-23 03:05 确认，Tibo 尚无 Done 帖）。这是预告，不是已落地确认；完成次数仍为 57。',
    change='出现 Done / “propagated” / Radar 实测落地 / 用户额度确认 → 记为已完成 #58 并退出预告态；窗口（01:00 BJ，或字面 PST 02:00）过后仍无落地证据 → 报「预告窗口已过，落地未核实」，不顺延。',
    hour_note='官方时点：北京时间 2026-10-24 01:00 前（PDT）；备选字面 PST：02:00 前。',
    sources=[X+'2113492187770175603',X+'2113492502355562875','https://codex-reset.com'])
  # post-Day17 estimate superseded by Day18 official teaser
  estimate_superseded=dict(made_bj='2026-10-23 03:06',window_start_bj='2026-10-24 15:00',window_end_bj='2026-10-27 15:00',
    verdict='已被 Day18 官方预告取代（估计窗口起点前出现官方「before 10am PST」+ small ship）',confidence='低-中',
    prior_hit=dict(made_bj='2026-10-21 09:58',window_start_bj='2026-10-21 15:00',window_end_bj='2026-10-24 15:00',
      verdict='命中：Day17 于 2026-10-23 01:00 BJ 前落地，位于该估计窗口内（期间被官方预告取代）',confidence='低-中'))
  data=dict(generated_at_bj=bj(NOW),sources=['https://x.com/thsottiaux','https://codex-reset.com/api/timeline','https://status.openai.com'],
   last_reset=ev[-1],days_since_last=round(since,2),stats_30d=s30,stats_all=sall,teaser_lag_hours_challenge=lags,teaser_lag_labels=lag_labels,forecast=fc,forecast_check=prev,estimate_superseded=estimate_superseded,pending=pending,events=ev,
   gaps=['status.openai.com 未纳入（仅作故障线，本页未抓取）','多数早期事件只有确认/官宣时间，无独立预告帖，预测时间=unknown','Day 10 未在 X 找到 Tibo 完成帖；实际时间取 Radar 实测 06:13Z','Radar 归档的 Day 8/10/13 时间为 Radar 实测落地时间，非确认帖时间','2026-03-04 的事件仅覆盖约 9% 用户，Radar 仍记为 reset，保留','静默重置仅 2026-08-25 一次被 Radar 收录；其他静默重置未知','banked reset 单独列出，不计入间隔','Day 15（10-20）Radar 只收录了官宣帖、没有实测落地时间，实际时间取帖子时间','2026-10-21 01:10 的 credits 补偿帖（约 4 万账户账单限额错误）不是全局重置，未计入次数','Day 17 已计入 #57：Radar/Tibo 尚无落地确认帖，依据为官方窗口（10:00 PDT = 01:00 BJ 前）＋用户 2026-10-23 03:05 BJ 确认额度刷新；实际时间取窗口上限','Day 18（10-23）仅为官方预告，尚未确认落地，未计入全局次数；「small ship」= 同日产品小发布，非 banked/credits；实际时间=unknown'],
   banked=[dict(date_bj=bj(P(e['announced_at'])),summary=e['summary'],url=e['url']) for e in radar['events'] if e['type']=='credits'],
   non_reset=[dict(date_bj='2026-10-21 01:10',kind='credits_compensation',summary='约 4 万账户周末账单限额配置错误已修复；受影响用户获 credits 补偿。这不是全局重置。',url='https://x.com/thsottiaux/status/2112592264686149749'),
              dict(date_bj='2026-10-23 12:47',kind='product_ship_teaser',summary='Day18 回复中的「small ship」指同日小产品发布，不是 credits/banked 额度包；全局重置本身仍待落地确认。',url='https://x.com/thsottiaux/status/2113492502355562875')])
  json.dump(data,open('data.json','w'),ensure_ascii=False,indent=1)
  print(s30,sall,lags,fc,len(ev))
d=open('data.json').read();open('index.html','w').write(open('tpl.html').read().replace('__DATA__',d));print('rendered index.html')
