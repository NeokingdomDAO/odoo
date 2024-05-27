/** @odoo-module */

import {useService} from "@web/core/utils/hooks";
import {onWillStart, onMounted} from "@odoo/owl";

export const NeokPOTRenderer = {
    setup() {
        this._super(...arguments);
        this.orm = useService("orm");
        this.lAction = useService("action");

        onWillStart(async () => {
            // fetch tasks before rendering the view
            await this._fetchViewData();
        });
        onMounted(() => {
            // initialize control buttons with visibility
            if (this.sShowPrevTasksBar) this.checkChipContainerOffset();
        });
    },
    async _fetchViewData() {
        // fetch action ids where this top bar can be rendered
        // check if top bar should be rendered
        try {
            this.sShowPrevTasksBar = this.env.model.root.__viewType !== 'form';
        } catch {
            this.sShowPrevTasksBar = true;
        }

        try {
            if (this.sShowPrevTasksBar) {
                const viableActionsIds = await this.orm.call("project.task", "get_pot_viable_ids", [], {});
                this.sShowPrevTasksBar = viableActionsIds.includes(this.env.config.actionId || -1);
            }
        } catch (e) {
            this.sShowPrevTasksBar = false;
        }

        // fetch previously opened tasks
        if (this.sShowPrevTasksBar) {
            const resTasks = await this.orm.call("project.task", "get_previously_opened_10_tasks", [], {});
            this.resTasks = resTasks;
        } else {
            this.resTasks = [];
        }
    },
    openTaskByNeokChip(taskId) {
        return this.lAction.doAction({
            res_model: 'project.task',
            views: [[false, 'form']],
            type: 'ir.actions.act_window',
            view_mode: 'form',
            view_id: false,
            target: 'current',
            res_id: taskId,
            context: {},
            domain: [],
        });
    },
    scrollNeokPotContainer(direction) {
        const container = document.querySelector('.neok-pot-chip-container');
        const scrollAmount = Math.round(container.offsetWidth / 1.25);
        const self = this;

        container.classList.add('neok-pot-chip-container-hfade');

        if (direction === 'prev') {
            this.customScrollTo(self, container, container.scrollLeft - scrollAmount, 625, function () {
                // update control buttons visibility
                self.checkChipContainerOffset(container);
                container.classList.remove('neok-pot-chip-container-hfade');
            });
        } else if (direction === 'next') {
            this.customScrollTo(self, container, container.scrollLeft + scrollAmount, 625, function () {
                // update control buttons visibility
                self.checkChipContainerOffset(container);
                container.classList.remove('neok-pot-chip-container-hfade');
            });
        }
    },
    checkChipContainerOffset(containerEl = false) {
        const prevButton = document.querySelector('.neok-pot-prev-btn');
        const nextButton = document.querySelector('.neok-pot-next-btn');

        if (!containerEl) {
            containerEl = document.querySelector('.neok-pot-chip-container');
        }

        if (containerEl.scrollLeft === 0) {
            prevButton.style.display = 'none';
            containerEl.classList.remove('neok-pot-chip-container-lfade');
        } else {
            prevButton.style.display = 'block';
            containerEl.classList.add('neok-pot-chip-container-lfade');
        }

        // if scrolled amount is 95% of the container width, hide the next button anyways
        // @TODO its bugging with 100%, need to check reason
        const scrolledAm = containerEl.scrollLeft + containerEl.offsetWidth;
        const scrolledPercent = scrolledAm / containerEl.scrollWidth;

        if (scrolledPercent >= 0.95) {
            nextButton.style.display = 'none';
            containerEl.classList.remove('neok-pot-chip-container-rfade');
        } else {
            nextButton.style.display = 'block';
            containerEl.classList.add('neok-pot-chip-container-rfade');
        }
    },
    easeInOutQuad(t, b, c, d) {
        t /= d / 2;

        if (t < 1) return c / 2 * t * t + b;

        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    },
    customScrollTo(ctx, element, to, duration, callback) {
        const start = element.scrollLeft,
            change = to - start,
            increment = 20;
        let currentTime = 0;

        const animateScroll = function () {
            currentTime += increment;
            element.scrollLeft = ctx.easeInOutQuad(currentTime, start, change, duration);

            if (currentTime < duration) {
                setTimeout(animateScroll, increment);
            } else {
                if (callback && typeof (callback) === 'function') {
                    callback();
                }
            }
        };

        animateScroll();
    }
};