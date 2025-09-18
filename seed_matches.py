from app.models import Match, BettingOdd
from app.extensions import db
from datetime import datetime, timedelta

# Tạo danh sách trận đấu
matches = [
    Match(team_a="Manchester United", team_b="Arsenal", kickoff=datetime.utcnow() + timedelta(hours=3)),
    Match(team_a="Real Madrid", team_b="Barcelona", kickoff=datetime.utcnow() + timedelta(hours=6)),
    Match(team_a="Bayern Munich", team_b="Dortmund", kickoff=datetime.utcnow() + timedelta(hours=9)),
]

# Thêm vào DB nếu chưa có
for match in matches:
    if not Match.query.filter_by(team_a=match.team_a, team_b=match.team_b).first():
        db.session.add(match)

db.session.commit()

# Tạo tỷ lệ cược cho từng trận
for match in Match.query.all():
    odds = [
        BettingOdd(match_id=match.id, odd_type="Châu Á", value=1.5),
        BettingOdd(match_id=match.id, odd_type="Tài Xỉu", value=2.75),
        BettingOdd(match_id=match.id, odd_type="1X2", value=2.1),
    ]
    for odd in odds:
        if not BettingOdd.query.filter_by(match_id=match.id, odd_type=odd.odd_type).first():
            db.session.add(odd)

db.session.commit()
print("✅ Seed Match & BettingOdd thành công")
