interface ScoreGaugeProps {
  score: number;
  threshold: number;
}

export function ScoreGauge({ score, threshold = 0.75 }: ScoreGaugeProps) {
  const clamped = Math.max(0, Math.min(1, score));
  const end = 306 * clamped;
  const color = clamped >= threshold ? "var(--color-danger)" : "var(--color-warn)";
  return (
    <div>
      <div>{clamped.toFixed(2)}</div>
      <svg width={90} height={50}>
        <path d="M10,40 A35,35 0 0,1 80,40" fill="none" stroke="var(--color-border)" strokeWidth={8} />
        <path d={`M10,40 A35,35 0 ${end > 180 ? 1 : 0},1 80,40`} fill="none" stroke={color} strokeWidth={8} />
      </svg>
    </div>
  );
}
