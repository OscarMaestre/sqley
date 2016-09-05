SELECT mod.nombre, mod.horas_semanales, g.nombre_grupo, ciclos.nivel_profesional
    from ciclos, modulos as mod, grupos as g, cursos as cur
        where
            mod.curso_id=cur.id
        and
            especialidad<>'PT'
        and
            g.curso_id=cur.id
        and
            cur.ciclo_id=ciclos.id
        
    order by horas_semanales desc, num_curso desc, nivel_profesional desc;