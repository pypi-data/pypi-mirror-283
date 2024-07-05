/*
 * Copyright (C) 2023 Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#include "mimir/datasets/faithful_abstraction.hpp"

#include "mimir/algorithms/BS_thread_pool.hpp"
#include "mimir/common/timers.hpp"

#include <algorithm>
#include <cstdlib>
#include <deque>

namespace mimir
{

/**
 * FaithfulAbstractState
 */

FaithfulAbstractState::FaithfulAbstractState(StateIndex index, State state, Certificate certificate) :
    m_index(index),
    m_state(state),
    m_certificate(std::move(certificate))
{
}

bool FaithfulAbstractState::operator==(const FaithfulAbstractState& other) const
{
    if (this != &other)
    {
        // FaithfulAbstractStates are unique by id within a FaithfulAbstraction;
        return (m_index == other.m_index);
    }
    return true;
}

size_t FaithfulAbstractState::hash() const
{
    // FaithfulAbstractStates are unique by id within a FaithfulAbstraction;
    return loki::hash_combine(m_id);
}

StateIndex FaithfulAbstractState::get_index() const { return m_index; }

State FaithfulAbstractState::get_state() const { return m_state; }

const Certificate& FaithfulAbstractState::get_certificate() const { return m_certificate; }

/**
 * FaithfulAbstraction
 */

FaithfulAbstraction::FaithfulAbstraction(bool mark_true_goal_literals,
                                         bool use_unit_cost_one,
                                         std::shared_ptr<PDDLParser> parser,
                                         std::shared_ptr<IAAG> aag,
                                         std::shared_ptr<SuccessorStateGenerator> ssg,
                                         FaithfulAbstractStateList states,
                                         StateMap<StateIndex> concrete_to_abstract_state,
                                         CertificateToStateIndexMap states_by_certificate,
                                         StateIndex initial_state,
                                         StateIndexSet goal_states,
                                         StateIndexSet deadend_states,
                                         AbstractTransitionList transitions,
                                         std::shared_ptr<GroundActionList> ground_actions_by_source_and_target,
                                         BeginIndexList transitions_begin_by_source,
                                         std::vector<double> goal_distances) :
    m_mark_true_goal_literals(mark_true_goal_literals),
    m_use_unit_cost_one(use_unit_cost_one),
    m_parser(std::move(parser)),
    m_aag(std::move(aag)),
    m_ssg(std::move(ssg)),
    m_states(std::move(states)),
    m_concrete_to_abstract_state(std::move(concrete_to_abstract_state)),
    m_states_by_certificate(std::move(states_by_certificate)),
    m_initial_state(initial_state),
    m_goal_states(std::move(goal_states)),
    m_deadend_states(std::move(deadend_states)),
    m_transitions(std::move(transitions)),
    m_ground_actions_by_source_and_target(std::move(ground_actions_by_source_and_target)),
    m_transitions_begin_by_source(std::move(transitions_begin_by_source)),
    m_goal_distances(std::move(goal_distances)),
    m_nauty_graph(),
    m_object_graph_factory(m_aag->get_problem(), m_parser->get_factories(), m_mark_true_goal_literals)
{
}

std::optional<FaithfulAbstraction> FaithfulAbstraction::create(const fs::path& domain_filepath,
                                                               const fs::path& problem_filepath,
                                                               bool mark_true_goal_literals,
                                                               bool use_unit_cost_one,
                                                               bool remove_if_unsolvable,
                                                               bool compute_complete_abstraction_mapping,
                                                               uint32_t max_num_states,
                                                               uint32_t timeout_ms)
{
    auto parser = std::make_shared<PDDLParser>(domain_filepath, problem_filepath);
    auto aag = std::make_shared<LiftedAAG>(parser->get_problem(), parser->get_factories());
    auto ssg = std::make_shared<SuccessorStateGenerator>(aag);

    return FaithfulAbstraction::create(std::move(parser),
                                       std::move(aag),
                                       std::move(ssg),
                                       mark_true_goal_literals,
                                       use_unit_cost_one,
                                       remove_if_unsolvable,
                                       compute_complete_abstraction_mapping,
                                       max_num_states,
                                       timeout_ms);
}

std::optional<FaithfulAbstraction> FaithfulAbstraction::create(std::shared_ptr<PDDLParser> parser,
                                                               std::shared_ptr<IAAG> aag,
                                                               std::shared_ptr<SuccessorStateGenerator> ssg,
                                                               bool mark_true_goal_literals,
                                                               bool use_unit_cost_one,
                                                               bool remove_if_unsolvable,
                                                               bool compute_complete_abstraction_mapping,
                                                               uint32_t max_num_states,
                                                               uint32_t timeout_ms)
{
    auto stop_watch = StopWatch(timeout_ms);

    const auto problem = parser->get_problem();
    const auto& factories = parser->get_factories();
    auto initial_state = ssg->get_or_create_initial_state();

    if (remove_if_unsolvable && !problem->static_goal_holds())
    {
        // Unsolvable
        return std::nullopt;
    }

    auto nauty_graph = nauty_wrapper::Graph();
    auto object_graph_factory = ObjectGraphFactory(problem, factories);
    auto concrete_to_abstract_state = StateMap<StateIndex> {};

    auto abstract_states = FaithfulAbstractStateList {};
    auto abstract_states_by_certificate = CertificateToStateIndexMap {};

    const auto abstract_initial_state_index = abstract_states.size();
    const auto& object_graph = object_graph_factory.create(initial_state);
    object_graph.get_digraph().to_nauty_graph(nauty_graph);
    auto certificate = Certificate(
        nauty_graph.compute_certificate(object_graph.get_partitioning().get_vertex_index_permutation(), object_graph.get_partitioning().get_partitioning()),
        object_graph.get_sorted_vertex_colors());
    abstract_states_by_certificate.emplace(certificate, abstract_initial_state_index);
    concrete_to_abstract_state.emplace(initial_state, abstract_initial_state_index);
    auto abstract_initial_state = FaithfulAbstractState(abstract_initial_state_index, initial_state, certificate);
    abstract_states.push_back(abstract_initial_state);

    auto lifo_queue = std::deque<State>();
    lifo_queue.push_back(initial_state);

    auto transitions = TransitionList {};
    auto abstract_goal_states = StateIndexSet {};

    auto applicable_actions = GroundActionList {};
    stop_watch.start();

    while (!lifo_queue.empty() && !stop_watch.has_finished())
    {
        const auto state = lifo_queue.back();
        const auto abstract_state_index = concrete_to_abstract_state.at(state);

        lifo_queue.pop_back();

        if (state.literals_hold(problem->get_goal_condition<Fluent>()) && state.literals_hold(problem->get_goal_condition<Derived>()))
        {
            abstract_goal_states.insert(abstract_state_index);
        }

        aag->generate_applicable_actions(state, applicable_actions);

        for (const auto& action : applicable_actions)
        {
            const auto successor_state = ssg->get_or_create_successor_state(state, action);

            // Regenerate concrete state
            const auto concrete_state_exists = concrete_to_abstract_state.count(successor_state);
            if (concrete_state_exists)
            {
                const auto& abstract_successor_state = abstract_states.at(concrete_to_abstract_state.at(successor_state));
                const auto abstract_successor_state_index = abstract_successor_state.get_index();
                transitions.emplace_back(abstract_successor_state_index, abstract_state_index, action);
                continue;
            }

            // Compute certificate of successor state
            const auto& object_graph = object_graph_factory.create(successor_state);
            object_graph.get_digraph().to_nauty_graph(nauty_graph);
            auto certificate = Certificate(nauty_graph.compute_certificate(object_graph.get_partitioning().get_vertex_index_permutation(),
                                                                           object_graph.get_partitioning().get_partitioning()),
                                           object_graph.get_sorted_vertex_colors());
            const auto it = abstract_states_by_certificate.find(certificate);

            // Regenerate abstract state
            const auto abstract_state_exists = (it != abstract_states_by_certificate.end());

            if (abstract_state_exists)
            {
                /* Add concrete state to abstraction mapping. */
                concrete_to_abstract_state.emplace(successor_state, it->second);
            }
            else
            {
                /* Generate new abstract state and add concrete state to abstraction mapping.  */
                const auto abstract_successor_state_index = abstract_states.size();
                const auto abstract_successor_state = FaithfulAbstractState(abstract_successor_state_index, successor_state, certificate);
                abstract_states.push_back(abstract_successor_state);
                abstract_states_by_certificate.emplace(certificate, abstract_successor_state_index);
                concrete_to_abstract_state.emplace(successor_state, abstract_successor_state_index);
                // Ensure that abstract states are stored by index.
                assert(abstract_states.back().get_index() == abstract_states.size() - 1);

                if (abstract_states.size() >= max_num_states)
                {
                    // Ran out of state resources
                    return std::nullopt;
                }
            }

            const auto abstract_successor_state_index = concrete_to_abstract_state.at(successor_state);
            transitions.emplace_back(abstract_successor_state_index, abstract_state_index, action);
            concrete_to_abstract_state.emplace(successor_state, abstract_successor_state_index);

            if (compute_complete_abstraction_mapping || !abstract_state_exists)
            {
                lifo_queue.push_back(successor_state);
            }
        }
    }

    if (stop_watch.has_finished())
    {
        // Ran out of time
        return std::nullopt;
    }

    if (remove_if_unsolvable && abstract_goal_states.empty())
    {
        // Skip: unsolvable
        return std::nullopt;
    }

    auto abstract_goal_distances = mimir::compute_shortest_goal_distances(abstract_states.size(), abstract_goal_states, transitions);

    auto abstract_deadend_states = StateIndexSet {};
    for (const auto& state : abstract_states)
    {
        if (abstract_goal_distances.at(state.get_index()) == std::numeric_limits<double>::max())
        {
            abstract_deadend_states.insert(state.get_index());
        }
    }

    /* Sort transitions by source and target state. */
    std::sort(transitions.begin(),
              transitions.end(),
              [](const auto& l, const auto& r)
              {
                  if (l.get_source_state() == r.get_source_state())
                  {
                      return l.get_target_state() < r.get_target_state();
                  }
                  return l.get_source_state() < r.get_source_state();
              });

    /* Store actions persistently and grouped by source and target to be able to use span. */
    auto ground_actions_by_source_and_target = std::make_shared<GroundActionList>();
    std::transform(transitions.begin(),
                   transitions.end(),
                   std::back_inserter(*ground_actions_by_source_and_target),
                   [](const auto& transition) { return transition.get_creating_action(); });

    /* Group transitions by source and target */
    auto transitions_begin_by_source_and_target = BeginIndexList {};
    // Set begin of first state index.
    transitions_begin_by_source_and_target.push_back(0);
    // Set begin of intermediate state indices.
    for (size_t i = 1; i < transitions.size(); ++i)
    {
        const auto& prev_transition = transitions.at(i - 1);
        const auto& cur_transition = transitions.at(i);

        if ((prev_transition.get_source_state() != cur_transition.get_source_state())  //
            || (prev_transition.get_target_state() != cur_transition.get_target_state()))
        {
            transitions_begin_by_source_and_target.push_back(i);
        }
    }
    // Set end of last state index.
    transitions_begin_by_source_and_target.push_back(transitions.size());

    /* Create abstract transitions from groups. */
    auto abstract_transitions = AbstractTransitionList {};
    for (size_t i = 0; i < transitions_begin_by_source_and_target.size() - 1; ++i)
    {
        const auto begin_offset = transitions_begin_by_source_and_target[i];
        const auto end_offset = transitions_begin_by_source_and_target[i + 1];

        bool has_transition = (begin_offset != end_offset);

        if (has_transition)
        {
            const auto src = (transitions.begin() + begin_offset)->get_source_state();
            const auto dst = (transitions.begin() + begin_offset)->get_target_state();

            abstract_transitions.emplace_back(src,
                                              dst,
                                              std::span<GroundAction>((*ground_actions_by_source_and_target).begin() + begin_offset,
                                                                      (*ground_actions_by_source_and_target).begin() + end_offset));
        }
    }

    /* Group abstract transitions by source. */
    auto transitions_begin_by_source = BeginIndexList {};
    // Set begin of first state index.
    transitions_begin_by_source.push_back(0);
    // Set begin of intermediate state indices.
    for (size_t i = 1; i < abstract_transitions.size(); ++i)
    {
        const auto& prev_transition = abstract_transitions.at(i - 1);
        const auto& cur_transition = abstract_transitions.at(i);
        if (prev_transition.get_source_state() != cur_transition.get_source_state())
        {
            transitions_begin_by_source.push_back(i);
        }
    }
    // Set end of last state index.
    transitions_begin_by_source.push_back(transitions.size());

    return FaithfulAbstraction(mark_true_goal_literals,
                               use_unit_cost_one,
                               std::move(parser),
                               std::move(aag),
                               std::move(ssg),
                               std::move(abstract_states),
                               std::move(concrete_to_abstract_state),
                               std::move(abstract_states_by_certificate),
                               abstract_initial_state_index,
                               std::move(abstract_goal_states),
                               std::move(abstract_deadend_states),
                               std::move(abstract_transitions),
                               std::move(ground_actions_by_source_and_target),
                               std::move(transitions_begin_by_source),
                               std::move(abstract_goal_distances));
}

std::vector<FaithfulAbstraction> FaithfulAbstraction::create(const fs::path& domain_filepath,
                                                             const std::vector<fs::path>& problem_filepaths,
                                                             bool mark_true_goal_literals,
                                                             bool use_unit_cost_one,
                                                             bool remove_if_unsolvable,
                                                             bool compute_complete_abstraction_mapping,
                                                             bool sort_ascending_by_num_states,
                                                             uint32_t max_num_states,
                                                             uint32_t timeout_ms,
                                                             uint32_t num_threads)
{
    auto memories = std::vector<std::tuple<std::shared_ptr<PDDLParser>, std::shared_ptr<IAAG>, std::shared_ptr<SuccessorStateGenerator>>> {};
    for (const auto& problem_filepath : problem_filepaths)
    {
        auto parser = std::make_shared<PDDLParser>(domain_filepath, problem_filepath);
        auto aag = std::make_shared<GroundedAAG>(parser->get_problem(), parser->get_factories());
        auto ssg = std::make_shared<SuccessorStateGenerator>(aag);
        memories.emplace_back(std::move(parser), std::move(aag), std::move(ssg));
    }

    return FaithfulAbstraction::create(memories,
                                       mark_true_goal_literals,
                                       use_unit_cost_one,
                                       remove_if_unsolvable,
                                       compute_complete_abstraction_mapping,
                                       sort_ascending_by_num_states,
                                       max_num_states,
                                       timeout_ms,
                                       num_threads);
}

std::vector<FaithfulAbstraction> FaithfulAbstraction::create(
    const std::vector<std::tuple<std::shared_ptr<PDDLParser>, std::shared_ptr<IAAG>, std::shared_ptr<SuccessorStateGenerator>>>& memories,
    bool mark_true_goal_literals,
    bool use_unit_cost_one,
    bool remove_if_unsolvable,
    bool compute_complete_abstraction_mapping,
    bool sort_ascending_by_num_states,
    uint32_t max_num_states,
    uint32_t timeout_ms,
    uint32_t num_threads)
{
    auto abstractions = std::vector<FaithfulAbstraction> {};
    auto pool = BS::thread_pool(num_threads);
    auto futures = std::vector<std::future<std::optional<FaithfulAbstraction>>> {};

    for (const auto& [parser, aag, ssg] : memories)
    {
        futures.push_back(pool.submit_task(
            [parser,
             aag,
             ssg,
             mark_true_goal_literals,
             use_unit_cost_one,
             remove_if_unsolvable,
             compute_complete_abstraction_mapping,
             max_num_states,
             timeout_ms]
            {
                return FaithfulAbstraction::create(parser,
                                                   aag,
                                                   ssg,
                                                   mark_true_goal_literals,
                                                   use_unit_cost_one,
                                                   remove_if_unsolvable,
                                                   compute_complete_abstraction_mapping,
                                                   max_num_states,
                                                   timeout_ms);
            }));
    }

    for (auto& future : futures)
    {
        auto abstraction = future.get();
        if (abstraction.has_value())
        {
            abstractions.push_back(std::move(abstraction.value()));
        }
    }

    if (sort_ascending_by_num_states)
    {
        std::sort(abstractions.begin(), abstractions.end(), [](const auto& l, const auto& r) { return l.get_num_states() < r.get_num_states(); });
    }

    return abstractions;
}

/**
 * Abstraction functionality
 */

StateIndex FaithfulAbstraction::get_abstract_state_index(State concrete_state)
{
    // Cheap test.
    if (m_concrete_to_abstract_state.count(concrete_state))
    {
        return m_concrete_to_abstract_state.at(concrete_state);
    }

    // Expensive test.
    const auto& object_graph = m_object_graph_factory.create(concrete_state);
    object_graph.get_digraph().to_nauty_graph(m_nauty_graph);
    return m_states_by_certificate.at(Certificate(
        m_nauty_graph.compute_certificate(object_graph.get_partitioning().get_vertex_index_permutation(), object_graph.get_partitioning().get_partitioning()),
        object_graph.get_sorted_vertex_colors()));
}

/**
 * Extended functionality
 */

std::vector<double> FaithfulAbstraction::compute_shortest_distances_from_states(const StateIndexList& abstract_states, bool forward) const
{
    throw std::runtime_error("Not implemented");
}

std::vector<std::vector<double>> FaithfulAbstraction::compute_pairwise_shortest_state_distances(bool forward) const
{
    throw std::runtime_error("Not implemented");
}

/**
 * Getters
 */

/* Meta data */
bool FaithfulAbstraction::get_mark_true_goal_literals() const { return m_mark_true_goal_literals; }

bool FaithfulAbstraction::get_use_unit_cost_one() const { return m_use_unit_cost_one; }

/* Memory */
const std::shared_ptr<PDDLParser>& FaithfulAbstraction::get_pddl_parser() const { return m_parser; }

const std::shared_ptr<IAAG>& FaithfulAbstraction::get_aag() const { return m_aag; }

const std::shared_ptr<SuccessorStateGenerator>& FaithfulAbstraction::get_ssg() const { return m_ssg; }

/* States */
const FaithfulAbstractStateList& FaithfulAbstraction::get_states() const { return m_states; }

const StateMap<StateIndex>& FaithfulAbstraction::get_concrete_to_abstract_state() const { return m_concrete_to_abstract_state; }

const CertificateToStateIndexMap& FaithfulAbstraction::get_states_by_certificate() const { return m_states_by_certificate; }

StateIndex FaithfulAbstraction::get_initial_state() const { return m_initial_state; }

const StateIndexSet& FaithfulAbstraction::get_goal_states() const { return m_goal_states; }

const StateIndexSet& FaithfulAbstraction::get_deadend_states() const { return m_deadend_states; }

TargetStateIterator<AbstractTransition> FaithfulAbstraction::get_target_states(StateIndex source) const
{
    return TargetStateIterator<AbstractTransition>(std::span<const AbstractTransition>(m_transitions.begin() + m_transitions_begin_by_source.at(source),
                                                                                       m_transitions.begin() + m_transitions_begin_by_source.at(source + 1)));
}

SourceStateIterator<AbstractTransition> FaithfulAbstraction::get_source_states(StateIndex target) const
{
    return SourceStateIterator<AbstractTransition>(target, std::span<const AbstractTransition>(m_transitions.begin(), m_transitions.end()));
}

size_t FaithfulAbstraction::get_num_states() const { return get_states().size(); }

size_t FaithfulAbstraction::get_num_goal_states() const { return get_goal_states().size(); }

size_t FaithfulAbstraction::get_num_deadend_states() const { return get_deadend_states().size(); }

bool FaithfulAbstraction::is_goal_state(StateIndex state) const { return get_goal_states().count(state); }

bool FaithfulAbstraction::is_deadend_state(StateIndex state) const { return get_deadend_states().count(state); }

bool FaithfulAbstraction::is_alive_state(StateIndex state) const { return !(get_goal_states().count(state) || get_deadend_states().count(state)); }

/* Transitions */
const AbstractTransitionList& FaithfulAbstraction::get_transitions() const { return m_transitions; }

const BeginIndexList& FaithfulAbstraction::get_transitions_begin_by_source() const { return m_transitions_begin_by_source; }

TransitionCost FaithfulAbstraction::get_transition_cost(TransitionIndex transition) const
{
    return (m_use_unit_cost_one) ? 1 : m_transitions.at(transition).get_cost();
}

ForwardTransitionIterator<AbstractTransition> FaithfulAbstraction::get_forward_transitions(StateIndex source) const
{
    return ForwardTransitionIterator<AbstractTransition>(
        std::span<const AbstractTransition>(m_transitions.begin() + m_transitions_begin_by_source.at(source),
                                            m_transitions.begin() + m_transitions_begin_by_source.at(source + 1)));
}

BackwardTransitionIterator<AbstractTransition> FaithfulAbstraction::get_backward_transitions(StateIndex target) const
{
    return BackwardTransitionIterator<AbstractTransition>(target, std::span<const AbstractTransition>(m_transitions.begin(), m_transitions.end()));
}

size_t FaithfulAbstraction::get_num_transitions() const { return m_transitions.size(); }

/* Distances */
const std::vector<double>& FaithfulAbstraction::get_goal_distances() const { return m_goal_distances; }

}
