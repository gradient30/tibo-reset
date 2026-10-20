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
  ev=[]
  for e in radar['events']:
    if e['type']!='reset' or e['source']!='archive': continue
    a=P(e['announced_at']); d=detail.get(e['id'])
    r=dict(id=e['id'],radar_url=e['url'],radar_summary=e['summary'],reasons=e['reason_tags'],
      actual_utc=a.isoformat(),actual_bj=bj(a),actual_basis='Radar 归档时间（确认帖或实测落地）',
      window=e['official_window'],label=None,teaser=None,predicted_bj='unknown',pred_note='无独立预告帖记录（多为直接官宣即落地）',lag_teaser_h=None,dev_h=None,confirmation=None)
    if e['official_window'] and e['official_window'].get('end_at'):
      pe=P(e['official_window']['end_at']); r['predicted_bj']=bj(pe)+'（截止）'; r['pred_note']='官方窗口：'+e['official_window']['label']; r['dev_h']=round((a-pe).total_seconds()/3600,2)
    if d:
      r['label']=d['label']; t=P(d['teaser'][1])
      r['teaser']=dict(url=X+d['teaser'][0],time_bj=bj(t),quote=d['teaser'][2])
      r['lag_teaser_h']=round((a-t).total_seconds()/3600,2)
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
  # forecast: challenge Day16-18 (PT days Oct 20-22) => BJT Oct 20 15:00 .. Oct 23 15:00, start no earlier than now
  ws=max(NOW,dt.datetime(2026,10,20,7,0,tzinfo=Z)); we=dt.datetime(2026,10,23,7,0,tzinfo=Z)
  fc=dict(window_start_bj=bj(ws),window_end_bj=bj(we),confidence='低-中',
   basis=f"28 天 ship-or-reset 挑战（2026-10-04 公布，Day1≈10-05 PT，约至 11-01）期内已兑现 Day2/6/8/10/13，间隔 4.0/2.0/2.0/2.6 天；近 30 天 {s30['n']} 个间隔中位数 {s30['median']} 天、均值 {s30['mean']} 天。距 Day13 已 {since:.1f} 天，Day14/15 为功能发布。窗口取 Day16–Day18（PT 10-20 至 10-22）≈ 中位间隔 + 散布余量。挑战期内，判据是 Tibo 当日的「Day N/ Reset」帖，预告到落地中位约 {st.median(lags):.1f} 小时。",
   change='出现「Day N/ Reset」帖即改为当日 PT 结束前（北京时间次日 15:00 前）；窗口过去无帖则撤回本预测，不顺延。',
   hour_note=f"近 30 天落地时刻（北京）：{sorted(hrs)} — 分散，不给固定时点")
  data=dict(generated_at_bj=bj(NOW),sources=['https://x.com/thsottiaux','https://codex-reset.com/api/timeline','https://status.openai.com'],
   last_reset=ev[-1],days_since_last=round(since,2),stats_30d=s30,stats_all=sall,teaser_lag_hours_challenge=lags,forecast=fc,events=ev,
   gaps=['status.openai.com 未纳入（仅作故障线，本页未抓取）','多数早期事件只有确认/官宣时间，无独立预告帖，预测时间=unknown','Day 10 未在 X 找到 Tibo 完成帖；实际时间取 Radar 实测 06:13Z','Radar 归档的 Day 8/10/13 时间为 Radar 实测落地时间，非确认帖时间','2026-03-04 的事件仅覆盖约 9% 用户，Radar 仍记为 reset，保留','静默重置仅 2026-08-25 一次被 Radar 收录；其他静默重置未知','banked reset 单独列出，不计入间隔'],
   banked=[dict(date_bj=bj(P(e['announced_at'])),summary=e['summary'],url=e['url']) for e in radar['events'] if e['type']=='credits'])
  json.dump(data,open('data.json','w'),ensure_ascii=False,indent=1)
  print(s30,sall,lags,fc,len(ev))
d=open('data.json').read();open('index.html','w').write(open('tpl.html').read().replace('__DATA__',d));print('rendered index.html')
