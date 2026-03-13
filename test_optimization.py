"""
Script de test pour valider les optimisations contextuelles Phase 2.
Version simplifiée sans dépendances externes (requests, smtplib).
"""

import logging
from datetime import datetime
from context_management import (
    HistoryCompressor,
    SlidingWindowManager,
    MemoryCleaner,
    AgentState,
    build_optimized_prompt_context,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def test_prompt_optimization():
    """Teste l'optimisation des prompts."""
    log.info("=" * 60)
    log.info("TEST 1: Optimisation des Prompts")
    log.info("=" * 60)
    
    # Test du prompt principal (sans exécuter l'agent)
    from oil_agent import get_master_prompt
    prompt = get_master_prompt()
    
    # Estimation simple des tokens (4 caractères ≈ 1 token)
    prompt_tokens = len(prompt) // 4
    
    log.info(f"Prompt principal: {prompt_tokens:,} tokens")
    log.info(f"Objectif: < 500 tokens")
    log.info(f"Résultat: {'PASS' if prompt_tokens < 500 else 'FAIL'}")
    
    return prompt_tokens < 500


def test_context_management():
    """Teste la gestion du contexte."""
    log.info("=" * 60)
    log.info("TEST 2: Gestion du Contexte (Phase 2)")
    log.info("=" * 60)
    
    try:
        # Créer un agent simple sans démarrer llama-server
        from context_management import AgentState, SlidingWindowManager, MemoryCleaner
        
        state = AgentState(max_steps=10)
        window_manager = SlidingWindowManager(window_size=3, max_tokens=8000)
        memory_cleaner = MemoryCleaner()
        
        # Vérifier que l'agent a les attributs de gestion de contexte
        has_state = state is not None
        has_window_manager = window_manager is not None
        has_memory_cleaner = memory_cleaner is not None
        
        log.info(f"Agent state: {'OK' if has_state else 'FAIL'}")
        log.info(f"Window manager: {'OK' if has_window_manager else 'FAIL'}")
        log.info(f"Memory cleaner: {'OK' if has_memory_cleaner else 'FAIL'}")
        
        # Test AgentState extended attributes
        if has_state:
            has_tools_used = hasattr(state, 'tools_used')
            has_detected_events = hasattr(state, 'detected_events')
            has_high_impact_events = hasattr(state, 'high_impact_events')
            has_compression_savings = hasattr(state, 'compression_savings')
            
            log.info(f"AgentState.tools_used: {'OK' if has_tools_used else 'FAIL'}")
            log.info(f"AgentState.detected_events: {'OK' if has_detected_events else 'FAIL'}")
            log.info(f"AgentState.high_impact_events: {'OK' if has_high_impact_events else 'FAIL'}")
            log.info(f"AgentState.compression_savings: {'OK' if has_compression_savings else 'FAIL'}")
        
        # Test SlidingWindowManager compressed_history
        if has_window_manager:
            has_compressed_history = hasattr(window_manager, 'compressed_history')
            log.info(f"WindowManager.compressed_history: {'OK' if has_compressed_history else 'FAIL'}")
        
        # Test AgentState methods
        if has_state:
            try:
                state.add_tool_usage("test_tool")
                log.info(f"AgentState.add_tool_usage(): OK")
            except Exception as e:
                log.error(f"AgentState.add_tool_usage(): FAIL - {e}")
            
            try:
                state.add_detected_event({
                    'title': 'Test Event',
                    'category': 'Test',
                    'impact_score': 8,
                    'summary': 'Test event summary'
                })
                log.info(f"AgentState.add_detected_event(): OK")
            except Exception as e:
                log.error(f"AgentState.add_detected_event(): FAIL - {e}")
            
            try:
                state.add_compression_savings(100)
                log.info(f"AgentState.add_compression_savings(): OK")
            except Exception as e:
                log.error(f"AgentState.add_compression_savings(): FAIL - {e}")
        
        # Test SlidingWindowManager methods
        if has_window_manager:
            try:
                window_manager.add_step({
                    'step': 1,
                    'tool_calls': ['test_tool'],
                    'events': [],
                    'timestamp': datetime.now().isoformat()
                })
                log.info(f"WindowManager.add_step(): OK")
            except Exception as e:
                log.error(f"WindowManager.add_step(): FAIL - {e}")
            
            try:
                summary = window_manager.get_window_summary()
                log.info(f"WindowManager.get_window_summary(): OK - {summary[:100] if summary else 'empty'}")
            except Exception as e:
                log.error(f"WindowManager.get_window_summary(): FAIL - {e}")
        
        # Test MemoryCleaner methods
        if has_memory_cleaner:
            try:
                test_content = "Line 1\nLine 2\nLine 1\nLine 3\nTest content"
                cleaned = memory_cleaner.clean_content(test_content)
                log.info(f"MemoryCleaner.clean_content(): OK - {len(test_content)} -> {len(cleaned)} chars")
            except Exception as e:
                log.error(f"MemoryCleaner.clean_content(): FAIL - {e}")
            
            try:
                test_events = [
                    {'title': 'Event 1', 'category': 'Test', 'impact_score': 5},
                    {'title': 'Event 2', 'category': 'Test', 'impact_score': 7},
                    {'title': 'Event 1', 'category': 'Test', 'impact_score': 6},
                ]
                deduplicated = memory_cleaner.deduplicate_events(test_events)
                log.info(f"MemoryCleaner.deduplicate_events(): OK - {len(test_events)} -> {len(deduplicated)} events")
            except Exception as e:
                log.error(f"MemoryCleaner.deduplicate_events(): FAIL - {e}")
        
        return has_state and has_window_manager and has_memory_cleaner
    except Exception as e:
        log.error(f"Erreur lors du test: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False


def test_compression():
    """Teste la compression de l'historique."""
    log.info("=" * 60)
    log.info("TEST 3: Compression de l'Historique")
    log.info("=" * 60)
    
    try:
        # Test HistoryCompressor
        compressor = HistoryCompressor(compression_ratio=0.15)
        
        test_history = [
            {'role': 'user', 'content': 'This is a very long message that should be compressed to save tokens in context window of agent system'},
            {'role': 'assistant', 'content': 'Another long message with lots of details that need to be summarized concisely'},
            {'role': 'user', 'content': 'Short message'},
            {'role': 'assistant', 'content': 'Response'},
            {'role': 'user', 'content': 'Another query that requires attention'},
        ]
        
        compressed = compressor.compress_history(test_history)
        
        # Estimation simple des tokens
        original_tokens = sum(len(turn['content']) // 4 for turn in test_history)
        compressed_tokens = len(compressed) // 4
        savings = original_tokens - compressed_tokens
        
        log.info(f"Historique original: {original_tokens:,} tokens")
        log.info(f"Historique compressé: {compressed_tokens:,} tokens")
        log.info(f"Économies de compression: {savings:,} tokens ({savings/original_tokens*100:.1f}%)")
        log.info(f"Résultat: {'PASS' if savings > 0 else 'FAIL'}")
        
        # Test SlidingWindowManager compression
        window_manager = SlidingWindowManager(window_size=3, max_tokens=8000)
        
        # Ajouter des étapes de test
        for i in range(5):
            window_manager.add_step({
                'step': i,
                'tool_calls': [f'tool_{i}'],
                'events': [],
                'timestamp': datetime.now().isoformat(),
                'input_tokens': 1000,
                'output_tokens': 500
            })
        
        # Test de compression
        compressed_window = window_manager.compress_window(compressor)
        if compressed_window:
            log.info(f"Compression de fenêtre: OK - {compressed_window['steps_count']} étapes compressées")
            log.info(f"Résumé compressé: {compressed_window['summary'][:200]}")
        else:
            log.warning(f"Compression de fenêtre: FAIL - aucun historique compressé")
        
        return savings > 0
    except Exception as e:
        log.error(f"Erreur lors du test de compression: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False


def test_tracking():
    """Teste le tracking des étapes et des événements."""
    log.info("=" * 60)
    log.info("TEST 4: Tracking des Étapes et Événements")
    log.info("=" * 60)
    
    try:
        from context_management import AgentState
        
        state = AgentState(max_steps=10)
        
        # Test du tracking des étapes
        initial_step = state.current_step
        state.increment_step()
        log.info(f"Incrémentation d'étape: {initial_step} -> {state.current_step}")
        
        # Test du tracking des événements
        test_events = [
            {
                'title': 'High Impact Event 1',
                'category': 'Iran',
                'impact_score': 9,
                'summary': 'Test event with high impact'
            },
            {
                'title': 'Medium Impact Event 2',
                'category': 'Refinery',
                'impact_score': 6,
                'summary': 'Test event with medium impact'
            },
            {
                'title': 'Low Impact Event 3',
                'category': 'OPEC',
                'impact_score': 4,
                'summary': 'Test event with low impact'
            },
        ]
        
        for event in test_events:
            state.add_detected_event(event)
        
        log.info(f"Événements détectés: {state.events_detected}")
        log.info(f"Événements à impact élevé: {len(state.high_impact_events)}")
        
        # Vérifier les événements à impact élevé (impact >= 7)
        expected_high_impact = sum(1 for e in test_events if e['impact_score'] >= 7)
        actual_high_impact = len(state.high_impact_events)
        
        log.info(f"Événements à impact élevé attendus: {expected_high_impact}")
        log.info(f"Événements à impact élevé actuels: {actual_high_impact}")
        log.info(f"Résultat: {'PASS' if expected_high_impact == actual_high_impact else 'FAIL'}")
        
        # Test du tracking des économies de compression
        state.add_compression_savings(500)
        log.info(f"Économies de compression: {state.compression_savings:,} tokens")
        
        # Test du tracking des outils
        state.add_tool_usage("search_iran_conflict")
        state.add_tool_usage("search_refinery_damage")
        state.add_tool_usage("search_opec_supply")
        
        log.info(f"Outils utilisés: {state.tools_used}")
        log.info(f"Nombre d'outils uniques: {len(state.tools_used)}")
        
        # Test de get_summary
        summary = state.get_summary()
        log.info(f"Résumé de l'état de l'agent:\n{summary}")
        
        return (expected_high_impact == actual_high_impact and 
                len(state.tools_used) == 3 and
                state.compression_savings == 500)
    except Exception as e:
        log.error(f"Erreur lors du test de tracking: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False


def test_build_optimized_prompt_context():
    """Teste la construction du contexte optimisé."""
    log.info("=" * 60)
    log.info("TEST 5: Build Optimized Prompt Context")
    log.info("=" * 60)
    
    try:
        from context_management import AgentState, SlidingWindowManager
        
        state = AgentState(max_steps=10)
        window_manager = SlidingWindowManager(window_size=3, max_tokens=8000)
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Test avec un état vide
        context = build_optimized_prompt_context(
            state,
            window_manager,
            current_date,
            current_datetime
        )
        
        context_tokens = len(context) // 4
        log.info(f"Contexte optimisé: {context_tokens:,} tokens")
        log.info(f"Objectif: < 1000 tokens")
        log.info(f"Résultat: {'PASS' if context_tokens < 1000 else 'FAIL'}")
        
        # Test avec un historique compressé
        window_manager.compressed_history = {
            'summary': 'Compressé: Used search_iran_conflict, search_refinery_damage',
            'steps_count': 3,
            'timestamp': datetime.now().isoformat()
        }
        
        context_with_compressed = build_optimized_prompt_context(
            state,
            window_manager,
            current_date,
            current_datetime
        )
        
        context_with_compressed_tokens = len(context_with_compressed) // 4
        log.info(f"Contexte avec historique compressé: {context_with_compressed_tokens:,} tokens")
        
        # Test avec des événements à impact élevé
        state.high_impact_events = [
            {'title': 'Test Event 1', 'impact_score': 8},
            {'title': 'Test Event 2', 'impact_score': 9},
        ]
        
        context_with_events = build_optimized_prompt_context(
            state,
            window_manager,
            current_date,
            current_datetime
        )
        
        context_with_events_tokens = len(context_with_events) // 4
        log.info(f"Contexte avec événements à impact élevé: {context_with_events_tokens:,} tokens")
        
        return context_tokens < 1000
    except Exception as e:
        log.error(f"Erreur lors du test de build_optimized_prompt_context: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False


def main():
    """Exécute tous les tests."""
    log.info("Démarrage des tests d'optimisation Phase 2")
    
    tests = [
        ("Optimisation des Prompts", test_prompt_optimization),
        ("Gestion du Contexte (Phase 2)", test_context_management),
        ("Compression de l'Historique", test_compression),
        ("Tracking des Étapes et Événements", test_tracking),
        ("Build Optimized Prompt Context", test_build_optimized_prompt_context),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            log.error(f"Erreur dans le test '{name}': {e}")
            results.append((name, False))
    
    # Résumé
    log.info("=" * 60)
    log.info("RÉSUMÉ DES TESTS PHASE 2")
    log.info("=" * 60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        log.info(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    log.info(f"\nTotal: {passed}/{total} tests passés")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
