#!/bin/bash
cd "$(dirname "$0")"

echo "=== Manim Example Player ==="
echo "1) CircleToSquare — วงกลมแปลงเป็นสี่เหลี่ยม"
echo "2) WritingEquation — สมการ Euler"
echo "3) MovingDot      — จุดวิ่งทิ้ง trace"
echo ""
read -p "เลือก (1-3): " choice

case $choice in
  1) SCENE="CircleToSquare" ;;
  2) SCENE="WritingEquation" ;;
  3) SCENE="MovingDot" ;;
  *) echo "ไม่รู้จัก"; exit 1 ;;
esac

echo "กำลัง render $SCENE..."
manim -ql example1.py $SCENE 2>/dev/null

FILE=$(find media/videos/example1 -name "${SCENE}.mp4" | head -1)
if [ -f "$FILE" ]; then
  echo "เปิดด้วย VLC..."
  vlc "$FILE" &
else
  echo "ไม่เจอไฟล์ mp4"
fi
