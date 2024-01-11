from values import Set, Stat, Stars, Quality, MaxValueStat6, MaxValueStat5


def calc_efficiency(rune):
    if rune.nb_stars == Stars.SIX.value or Stars.SIX_ANTIC.value:
        eff_main = 1
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (
                MaxValueStat6[Stat(rune.innate_stat_id).name].value * 5
            )
        for substat in rune.substats:
            if substat.value != Stat.NONE.value:
                eff_subs += (substat.value + substat.grind) / (
                    MaxValueStat6[Stat(substat.stat_id).name].value * 5
                )
        return round(((eff_main + eff_innate + eff_subs) / 2.8) * 100, 2)
    if rune.nb_stars == Stars.FIVE.value or Stars.FIVE_ANTIC.value:
        eff_main = 1  # to change
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (
                MaxValueStat5[Stat(rune.innate_stat_id).name].value * 5
            )
        for substat in rune.substats:
            if substat.value != Stat.NONE.value:
                eff_subs += (substat.value + substat.grind) / (
                    MaxValueStat5[Stat(substat.stat_id).name].value * 5
                )
        return round(((eff_main + eff_innate + eff_subs) / 2.8) * 100, 2)